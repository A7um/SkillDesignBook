#!/usr/bin/env python3
"""research.py — refresh the book's empirical foundation in one command.

The book is grounded in measurements of the top-1000 downloaded ClawHub
skills. Those measurements go stale. This tool keeps them fresh.

  research.py            # full pipeline: fetch -> analyze -> compare -> validate
  research.py fetch      # just snapshot the top-1000 to research/snapshots/
  research.py analyze    # recompute pattern frequencies on the latest snapshot
  research.py compare    # diff latest snapshot against previous
  research.py validate   # verify every skill citation in book/ still resolves

Output:
  research/snapshots/<date>.json   — raw data for future diffs
  research/reports/<date>.md       — human-readable report per cycle

Scripts are under research/ not /tmp/; this is the authoritative location.
Pipeline is intentionally strict: fail fast, produce structured output, let
the human decide what to act on.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Iterable

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
RESEARCH_DIR = REPO_ROOT / "research"
SNAPSHOTS_DIR = RESEARCH_DIR / "snapshots"
REPORTS_DIR = RESEARCH_DIR / "reports"
BOOK_DIR = REPO_ROOT / "book"

# ClawHub listing API — used purely read-only. Requires a UA header.
CLAWHUB_API = "https://clawhub.atomicbot.ai/api/skills"
CLAWHUB_PAGE_SIZE = 50
CLAWHUB_TARGET = 1000  # top-N to snapshot
HTTP_HEADERS = {"User-Agent": "SkillDesignBook-research/1.0"}
HTTP_TIMEOUT = 20

# Optional: used to match API slugs to local SKILL.md files.
# Defaulted to a sibling path; safe to leave unset.
SKILLS_REPO = Path(os.environ.get("SKILLS_REPO", "/tmp/clawhub-skills/skills"))

# Significance thresholds — the "do not churn" discipline.
# These are the rules by which the tool decides what's worth reporting.
THRESHOLDS = {
    "frequency_shift_pp": 5.0,       # report pattern freq shifts >= 5pp
    "new_top20_threshold": 20,       # top N skills whose novelty is interesting
    "pattern_candidate_min": 3,      # track candidates with 3+ skills
    "pattern_add_min": 5,            # actual add requires 5+ skills
}

# Patterns detected via regex across SKILL.md content.
# Keep this list aligned with book/04-skill-patterns.md so the numbers
# published in the book always match what this tool reports.
PATTERN_DETECTORS: dict[str, str] = {
    "when_to_use":       r"when to use",
    "when_not":          r"when not|don.t use|not for|never use this",
    "quick_start":       r"quick start|quick reference|getting started",
    "output_format":     r"output format|output template|report format",
    "workflow_section":  r"##\s+workflow|##\s+process|##\s+phases|##\s+steps",
    "troubleshooting":   r"troubleshoot|common errors|known issues",
    "error_handling":    r"error handling|if.*fails|when.*fails",
    "traps":             r"common traps|gotchas|pitfalls|common mistakes",
    "checklist":         r"\[ \]",
    "contrast":          r"[❌✅]|GOOD:|BAD:",
    "arrow_notation":    r"→",
    "emdash_rationale":  r" — ",
    "security_privacy":  r"security.*privacy|external endpoints|data.*leaves",
    "related_skills":    r"related skills|see also|complementary skills",
    "approval_gate":     r"ask.*approval|ask.*confirm|pause.*until",
    "core_rules":        r"core rules|key rules|critical rules",
    "memory_directory":  r"~/\w+/",
    "numbered_steps":    r"(?m)^1\.\s",
    "ai_mistakes":       r"ai mistake|agent mistake",
    "red_flags":         r"red flags|warning signs",
    "rationalizations":  r"rationalization|excuse.*reality",
    "never_emphasis":    r"\bNEVER\b|DO NOT\b",
    "always_emphasis":   r"\bALWAYS\b|\bMUST\b",
}

# --------------------------------------------------------------------------
# Data structures
# --------------------------------------------------------------------------


@dataclass
class Skill:
    """A single top-1000 entry with the SKILL.md facts we care about."""
    slug: str
    owner: str
    downloads: int
    stars: int
    installs: int
    lines: int = 0
    sections: int = 0
    code_blocks: int = 0
    has_scripts: bool = False
    script_count: int = 0
    has_refs: bool = False
    ref_count: int = 0
    content_found: bool = False
    pattern_hits: dict[str, bool] = field(default_factory=dict)


@dataclass
class Snapshot:
    """Everything about one fetch cycle. Serializable; written as JSON."""
    date: str
    source: str
    target_n: int
    fetched_n: int
    matched_n: int
    skills: list[Skill]
    threshold_config: dict[str, float]

    def to_dict(self) -> dict:
        d = asdict(self)
        # Let skills stay as plain dicts via asdict().
        return d


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------


def log(msg: str) -> None:
    print(f"[research] {msg}", file=sys.stderr)


def die(msg: str, code: int = 1) -> None:
    print(f"[research] error: {msg}", file=sys.stderr)
    sys.exit(code)


def today() -> str:
    return date.today().isoformat()


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers=HTTP_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        die(f"HTTP {e.code} from {url}")
    except urllib.error.URLError as e:
        die(f"network error fetching {url}: {e.reason}")
    return {}  # unreachable


def http_head_ok(url: str) -> bool:
    try:
        req = urllib.request.Request(url, headers=HTTP_HEADERS, method="HEAD")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return 200 <= resp.status < 400
    except Exception:
        return False


# --------------------------------------------------------------------------
# Fetch phase: API -> Snapshot (without SKILL.md body yet)
# --------------------------------------------------------------------------


def fetch_top_skills() -> list[dict]:
    """Return CLAWHUB_TARGET items from the API, sorted by downloads desc."""
    items: list[dict] = []
    pages = (CLAWHUB_TARGET + CLAWHUB_PAGE_SIZE - 1) // CLAWHUB_PAGE_SIZE
    for page in range(1, pages + 1):
        url = f"{CLAWHUB_API}?sort=downloads&dir=desc&limit={CLAWHUB_PAGE_SIZE}&page={page}"
        log(f"fetching page {page}/{pages}")
        data = http_get_json(url)
        batch = data.get("items") or []
        if not batch:
            log(f"page {page} returned empty — stopping early")
            break
        items.extend(batch)
        if len(items) >= CLAWHUB_TARGET:
            break
    return items[:CLAWHUB_TARGET]


# --------------------------------------------------------------------------
# Analyze phase: attach SKILL.md facts + pattern hits to each Skill
# --------------------------------------------------------------------------


def find_skill_file(slug: str, owner: str) -> Path | None:
    """Locate a SKILL.md for (owner, slug). Tries the expected path first,
    falls back to a slug-only search if the owner doesn't match the repo layout.
    """
    candidates = [SKILLS_REPO / owner / slug / "SKILL.md",
                  SKILLS_REPO / owner / slug / "skill.md"]
    for c in candidates:
        if c.exists():
            return c
    if not SKILLS_REPO.exists():
        return None
    # Slower fallback: check every author directory.
    for author_dir in SKILLS_REPO.iterdir():
        if not author_dir.is_dir():
            continue
        for fn in ("SKILL.md", "skill.md"):
            p = author_dir / slug / fn
            if p.exists():
                return p
    return None


def analyze_content(path: Path) -> dict:
    content = path.read_text(encoding="utf-8", errors="ignore")
    lines = content.count("\n") + 1
    sections = len(re.findall(r"^##\s+", content, re.MULTILINE))
    code_blocks = content.count("```") // 2
    pattern_hits = {
        name: bool(re.search(pat, content, re.IGNORECASE))
        for name, pat in PATTERN_DETECTORS.items()
    }
    return {
        "lines": lines,
        "sections": sections,
        "code_blocks": code_blocks,
        "pattern_hits": pattern_hits,
    }


def build_skills(api_items: Iterable[dict]) -> list[Skill]:
    skills: list[Skill] = []
    matched = 0
    for item in api_items:
        slug = item.get("slug") or ""
        owner = (item.get("owner") or {}).get("handle") or ""
        stats = item.get("stats") or {}
        s = Skill(
            slug=slug,
            owner=owner,
            downloads=int(stats.get("downloads") or 0),
            stars=int(stats.get("stars") or 0),
            installs=int(stats.get("installsAllTime") or stats.get("installs") or 0),
        )
        path = find_skill_file(slug, owner)
        if path is not None:
            s.content_found = True
            matched += 1
            ca = analyze_content(path)
            s.lines = ca["lines"]
            s.sections = ca["sections"]
            s.code_blocks = ca["code_blocks"]
            s.pattern_hits = ca["pattern_hits"]
            skill_dir = path.parent
            scripts_dir = skill_dir / "scripts"
            refs_dir = skill_dir / "references"
            if scripts_dir.is_dir():
                s.has_scripts = True
                s.script_count = sum(1 for _ in scripts_dir.iterdir())
            if refs_dir.is_dir():
                s.has_refs = True
                s.ref_count = sum(1 for _ in refs_dir.iterdir())
        skills.append(s)
    log(f"matched {matched}/{len(skills)} skills to SKILL.md files")
    return skills


# --------------------------------------------------------------------------
# Compare phase: snapshot diff
# --------------------------------------------------------------------------


@dataclass
class SnapshotDiff:
    new_top20: list[Skill]
    dropped_from_top1000: list[dict]  # previous skills no longer in current
    frequency_shifts: list[tuple[str, float, float, float]]  # name, prev, curr, delta
    pattern_candidates: list[tuple[str, int]]  # name, skill count (3 <= n < 5)


def compute_frequencies(skills: list[Skill]) -> dict[str, float]:
    """Return percentage (0-100) of skills exhibiting each pattern, matched only."""
    matched = [s for s in skills if s.content_found]
    if not matched:
        return {name: 0.0 for name in PATTERN_DETECTORS}
    return {
        name: 100.0 * sum(1 for s in matched if s.pattern_hits.get(name)) / len(matched)
        for name in PATTERN_DETECTORS
    }


def diff_snapshots(curr: Snapshot, prev: Snapshot | None) -> SnapshotDiff:
    curr_by_slug = {s.slug: s for s in curr.skills}
    prev_skills: list[Skill] = prev.skills if prev else []
    prev_by_slug = {s.slug: s for s in prev_skills}

    # New entrants into top-20 that weren't in the previous top-20.
    prev_top20_slugs = {s.slug for s in prev_skills[: THRESHOLDS["new_top20_threshold"]]}
    new_top20 = [
        s for s in curr.skills[: THRESHOLDS["new_top20_threshold"]]
        if s.slug not in prev_top20_slugs
    ]

    # Skills that were in prev snapshot but not in current — dropped citations risk.
    dropped = [
        {"slug": s.slug, "downloads": s.downloads}
        for s in prev_skills
        if s.slug not in curr_by_slug
    ]

    # Pattern frequency shifts.
    shifts: list[tuple[str, float, float, float]] = []
    curr_freq = compute_frequencies(curr.skills)
    prev_freq = compute_frequencies(prev_skills) if prev else {}
    for name, curr_pct in curr_freq.items():
        prev_pct = prev_freq.get(name, 0.0)
        delta = curr_pct - prev_pct
        if abs(delta) >= THRESHOLDS["frequency_shift_pp"]:
            shifts.append((name, prev_pct, curr_pct, delta))
    shifts.sort(key=lambda x: abs(x[3]), reverse=True)

    # Pattern candidates: hit by 3-4 skills in the top-20 (promising but not yet).
    # We scan only the top-20 because rare patterns that show up in top skills
    # are more interesting than common patterns spread thinly.
    top20 = curr.skills[:20]
    candidate_counts: dict[str, int] = {}
    for s in top20:
        for name, hit in s.pattern_hits.items():
            if hit:
                candidate_counts[name] = candidate_counts.get(name, 0) + 1
    candidates = [
        (name, cnt) for name, cnt in candidate_counts.items()
        if THRESHOLDS["pattern_candidate_min"] <= cnt < THRESHOLDS["pattern_add_min"]
    ]
    candidates.sort(key=lambda x: -x[1])

    return SnapshotDiff(
        new_top20=new_top20,
        dropped_from_top1000=dropped,
        frequency_shifts=shifts,
        pattern_candidates=candidates,
    )


def _skill_from_dict(d: dict) -> Skill:
    """Rehydrate a Skill from the JSON form used in snapshots."""
    fields = {k: d.get(k) for k in Skill.__dataclass_fields__}
    fields["pattern_hits"] = d.get("pattern_hits") or {}
    fields["lines"] = int(d.get("lines") or 0)
    fields["sections"] = int(d.get("sections") or 0)
    fields["code_blocks"] = int(d.get("code_blocks") or 0)
    fields["script_count"] = int(d.get("script_count") or 0)
    fields["ref_count"] = int(d.get("ref_count") or 0)
    fields["has_scripts"] = bool(d.get("has_scripts"))
    fields["has_refs"] = bool(d.get("has_refs"))
    fields["content_found"] = bool(d.get("content_found"))
    return Skill(**fields)


# --------------------------------------------------------------------------
# Validate phase: check book citations still resolve
# --------------------------------------------------------------------------

CITATION_RE = re.compile(r"\[([^\]]+)\]\(https://clawhub\.ai/skills/([^)]+)\)")


def find_book_citations(book_dir: Path) -> list[tuple[Path, str, str]]:
    out: list[tuple[Path, str, str]] = []
    for md in book_dir.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for m in CITATION_RE.finditer(text):
            out.append((md.relative_to(REPO_ROOT), m.group(1), m.group(2)))
    return out


def validate_citations(skills: list[Skill], book_dir: Path) -> list[tuple[Path, str, str, str]]:
    """Return (file, label, slug, reason) for every citation that no longer resolves."""
    live_slugs = {s.slug for s in skills}
    broken: list[tuple[Path, str, str, str]] = []
    for file, label, slug in find_book_citations(book_dir):
        if slug in live_slugs:
            continue
        reason = "not in top-1000" if http_head_ok(f"https://clawhub.ai/skills/{slug}") else "404"
        broken.append((file, label, slug, reason))
    return broken


# --------------------------------------------------------------------------
# Snapshot persistence
# --------------------------------------------------------------------------


def save_snapshot(snap: Snapshot) -> Path:
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOTS_DIR / f"{snap.date}.json"
    path.write_text(json.dumps(snap.to_dict(), indent=2))
    return path


def load_latest_snapshot(exclude: Path | None = None) -> Snapshot | None:
    if not SNAPSHOTS_DIR.exists():
        return None
    candidates = sorted(p for p in SNAPSHOTS_DIR.glob("*.json") if p != exclude)
    if not candidates:
        return None
    data = json.loads(candidates[-1].read_text())
    skills = [_skill_from_dict(s) for s in data.get("skills") or []]
    data["skills"] = skills
    return Snapshot(**{k: data.get(k) for k in Snapshot.__dataclass_fields__})


# --------------------------------------------------------------------------
# Report rendering
# --------------------------------------------------------------------------


def render_report(
    snap: Snapshot,
    diff: SnapshotDiff,
    broken_citations: list[tuple[Path, str, str, str]],
) -> str:
    lines: list[str] = []
    lines.append(f"# Book Update Report — {snap.date}\n")
    lines.append(f"- Source: `{snap.source}`")
    lines.append(f"- Fetched: {snap.fetched_n} skills (target {snap.target_n})")
    lines.append(f"- Matched to SKILL.md: {snap.matched_n}")
    lines.append("")

    lines.append("## Frequency shifts exceeding threshold\n")
    if diff.frequency_shifts:
        lines.append("| Pattern | Previous | Current | Delta |")
        lines.append("|---|---:|---:|---:|")
        for name, prev, curr, delta in diff.frequency_shifts:
            sign = "+" if delta >= 0 else ""
            lines.append(f"| `{name}` | {prev:.1f}% | {curr:.1f}% | {sign}{delta:.1f}pp |")
    else:
        lines.append(f"_None. All pattern frequencies within ±{THRESHOLDS['frequency_shift_pp']:.0f}pp of previous snapshot._")
    lines.append("")

    lines.append("## New entrants into top 20\n")
    if diff.new_top20:
        for s in diff.new_top20:
            lines.append(f"- **{s.slug}** — {s.downloads:,} downloads, {s.lines} lines, {s.sections} sections, scripts={s.script_count}, refs={s.ref_count}")
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("## Pattern candidates (3–4 hits in top 20; not yet at threshold)\n")
    if diff.pattern_candidates:
        for name, cnt in diff.pattern_candidates:
            lines.append(f"- `{name}`: {cnt} skills in top 20 (need ≥{THRESHOLDS['pattern_add_min']} to qualify for the book)")
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("## Citations in `book/` no longer resolving\n")
    if broken_citations:
        for file, label, slug, reason in broken_citations:
            lines.append(f"- `{file}` → [{label}](https://clawhub.ai/skills/{slug}) — **{reason}**")
    else:
        lines.append("_None. All cited skills still resolve._")
    lines.append("")

    lines.append("## Skills previously in top-1000 that dropped out\n")
    if diff.dropped_from_top1000:
        for d in diff.dropped_from_top1000[:50]:
            lines.append(f"- `{d['slug']}` (was {d['downloads']:,} dl)")
        if len(diff.dropped_from_top1000) > 50:
            lines.append(f"- _…and {len(diff.dropped_from_top1000) - 50} more._")
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("## Top 20 by downloads (current snapshot)\n")
    lines.append("| Rank | Skill | Downloads | Lines | Scripts | Refs |")
    lines.append("|---:|---|---:|---:|---:|---:|")
    for i, s in enumerate(snap.skills[:20], 1):
        lines.append(f"| {i} | [{s.slug}](https://clawhub.ai/skills/{s.slug}) | {s.downloads:,} | {s.lines} | {s.script_count} | {s.ref_count} |")
    lines.append("")

    lines.append("---\n")
    lines.append(
        "Recommended next steps: review the shifts and new entrants above, "
        "then consult `UPDATE_GUIDE.md` for the per-chapter update policy. "
        "Do not edit philosophy chapters without multi-skill convergence.\n"
    )
    return "\n".join(lines)


def save_report(text: str, snap_date: str) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / f"{snap_date}.md"
    path.write_text(text)
    return path


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------


def cmd_fetch(_: argparse.Namespace) -> int:
    api_items = fetch_top_skills()
    log(f"fetched {len(api_items)} skills from API")
    skills = build_skills(api_items)
    matched = sum(1 for s in skills if s.content_found)
    snap = Snapshot(
        date=today(),
        source=CLAWHUB_API,
        target_n=CLAWHUB_TARGET,
        fetched_n=len(skills),
        matched_n=matched,
        skills=skills,
        threshold_config=THRESHOLDS,
    )
    path = save_snapshot(snap)
    log(f"snapshot saved: {path.relative_to(REPO_ROOT)}")
    return 0


def cmd_analyze(_: argparse.Namespace) -> int:
    snap = load_latest_snapshot()
    if snap is None:
        die("no snapshot exists — run `research.py fetch` first")
    freq = compute_frequencies(snap.skills)
    print(f"# Pattern frequencies on snapshot {snap.date}\n")
    print("| Pattern | % of matched top-1000 |")
    print("|---|---:|")
    for name, pct in sorted(freq.items(), key=lambda x: -x[1]):
        print(f"| `{name}` | {pct:.1f}% |")
    return 0


def cmd_compare(_: argparse.Namespace) -> int:
    snapshots = sorted(SNAPSHOTS_DIR.glob("*.json")) if SNAPSHOTS_DIR.exists() else []
    if len(snapshots) < 2:
        die("need at least two snapshots to compare — run `fetch` again on a different date")
    curr = load_latest_snapshot()
    prev = load_latest_snapshot(exclude=snapshots[-1])
    diff = diff_snapshots(curr, prev)
    broken = validate_citations(curr.skills, BOOK_DIR)
    report = render_report(curr, diff, broken)
    print(report)
    return 0


def cmd_validate(_: argparse.Namespace) -> int:
    snap = load_latest_snapshot()
    if snap is None:
        die("no snapshot exists — run `research.py fetch` first")
    broken = validate_citations(snap.skills, BOOK_DIR)
    if not broken:
        print("All citations resolve.")
        return 0
    print(f"# Broken citations ({len(broken)})\n")
    for file, label, slug, reason in broken:
        print(f"- `{file}` → [{label}](https://clawhub.ai/skills/{slug}) — {reason}")
    return 1


def cmd_default(_: argparse.Namespace) -> int:
    """Full pipeline: fetch -> analyze -> compare -> validate -> write report."""
    api_items = fetch_top_skills()
    log(f"fetched {len(api_items)} skills from API")
    skills = build_skills(api_items)
    matched = sum(1 for s in skills if s.content_found)
    snap = Snapshot(
        date=today(),
        source=CLAWHUB_API,
        target_n=CLAWHUB_TARGET,
        fetched_n=len(skills),
        matched_n=matched,
        skills=skills,
        threshold_config=THRESHOLDS,
    )
    path = save_snapshot(snap)
    log(f"snapshot: {path.relative_to(REPO_ROOT)}")

    prev = load_latest_snapshot(exclude=path)
    diff = diff_snapshots(snap, prev)
    broken = validate_citations(snap.skills, BOOK_DIR)

    report = render_report(snap, diff, broken)
    report_path = save_report(report, snap.date)
    log(f"report: {report_path.relative_to(REPO_ROOT)}")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="research.py", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd")
    cmds: dict[str, Callable[[argparse.Namespace], int]] = {
        "fetch":    cmd_fetch,
        "analyze":  cmd_analyze,
        "compare":  cmd_compare,
        "validate": cmd_validate,
    }
    for name, fn in cmds.items():
        sp = sub.add_parser(name, help=fn.__doc__)
        sp.set_defaults(func=fn)
    p.set_defaults(func=cmd_default)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
