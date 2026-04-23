#!/usr/bin/env python3
"""research.py — the cheap-and-quantitative half of the book update pipeline.

This script does what pattern matching is good at:
  - counting known patterns across 1,000 skills
  - detecting citation decay
  - finding top-20 entrants
  - surfacing pattern candidates approaching threshold

It does NOT decide what's a new pattern. Regex can't read a skill
and notice that 5 skills are converging on a structure no existing
detector knows about. That's the agent's job.

The output is a *worklist* — a small, curated set of skills for the
agent to actually read. The agent's judgment, not this script's count,
determines whether the book should change.

Usage:
  research.py            # full pipeline: fetch -> analyze -> compare -> worklist -> validate
  research.py fetch      # snapshot the top-1000 to research/snapshots/
  research.py analyze    # recompute pattern frequencies on the latest snapshot
  research.py compare    # diff latest snapshot against previous
  research.py worklist   # emit the skills the agent should read next
  research.py validate   # verify every skill citation in book/ still resolves

Output:
  research/snapshots/<date>.json   — raw data for future diffs
  research/reports/<date>.md       — per-cycle quantitative report
  research/worklists/<date>.md     — curated skills for the agent to read

Pipeline is intentionally strict: fail fast on errors, produce structured
output, never silently skip. The agent and the human both rely on the
numbers being honest; a silent skip corrupts the book permanently.
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
WORKLISTS_DIR = RESEARCH_DIR / "worklists"
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
    "worklist_top_n": 20,            # always read the top-N by downloads
    "worklist_new_entrants": 10,     # plus the N most recent top-20 entrants
    "worklist_outlier_count": 10,    # plus N skills with unusual structure
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
# Worklist: the curated set of skills the agent should actually read
# --------------------------------------------------------------------------


def _skill_fingerprint(s: Skill) -> tuple:
    """A rough structural shape. Skills with unusual fingerprints among the
    top 1,000 are candidates for agent reading — they may use patterns the
    regex detectors don't know about."""
    hit_count = sum(1 for v in s.pattern_hits.values() if v)
    return (
        s.lines // 100,        # size bucket
        s.sections // 5,       # structure bucket
        s.code_blocks // 10,   # density bucket
        s.script_count,
        hit_count,
    )


def select_outliers(skills: list[Skill], n: int) -> list[Skill]:
    """Return N skills that look structurally unlike their neighbors.

    Heuristic: skills whose fingerprint is rare among the top 1,000 AND
    that match fewer known patterns than average are the most likely to
    be inventing something the detectors miss. Ranked by downloads so
    the agent's attention goes to skills users actually use.
    """
    matched = [s for s in skills if s.content_found]
    if not matched:
        return []
    fingerprints: dict[tuple, int] = {}
    for s in matched:
        fp = _skill_fingerprint(s)
        fingerprints[fp] = fingerprints.get(fp, 0) + 1
    avg_hits = sum(sum(v for v in s.pattern_hits.values()) for s in matched) / len(matched)
    scored = []
    for s in matched:
        fp = _skill_fingerprint(s)
        rarity = 1.0 / fingerprints[fp]
        hit_count = sum(1 for v in s.pattern_hits.values() if v)
        under_matched = max(0.0, avg_hits - hit_count) / max(avg_hits, 1.0)
        # Downloads as a log-scale tiebreaker, but rarity dominates.
        score = rarity * 10 + under_matched * 3 + (s.downloads / 1_000_000)
        scored.append((score, s))
    scored.sort(key=lambda x: -x[0])
    return [s for _, s in scored[:n]]


def build_worklist(
    curr: Snapshot,
    diff: "SnapshotDiff",
) -> dict[str, list[Skill]]:
    """Pick the skills the agent should read this cycle, grouped by reason."""
    top_n = THRESHOLDS["worklist_top_n"]
    new_count = THRESHOLDS["worklist_new_entrants"]
    outlier_count = THRESHOLDS["worklist_outlier_count"]

    top = curr.skills[:top_n]
    new_entrants = diff.new_top20[:new_count]
    seen = {s.slug for s in top} | {s.slug for s in new_entrants}
    outliers = [s for s in select_outliers(curr.skills, outlier_count * 2) if s.slug not in seen][:outlier_count]

    return {
        "top": top,
        "new_entrants": new_entrants,
        "outliers": outliers,
    }


def render_worklist(
    snap: Snapshot,
    groups: dict[str, list[Skill]],
    diff: "SnapshotDiff",
) -> str:
    """Produce an agent-facing Markdown worklist.

    The agent reads this, opens each linked SKILL.md, and answers three
    questions per skill:
      1. Does this skill use a structural pattern not in Chapter 4?
      2. Does it quote a principle that belongs in Chapter 1?
      3. If cited in the book, is the citation still accurate?
    """
    lines: list[str] = []
    lines.append(f"# Agent Worklist — {snap.date}\n")
    lines.append(
        "This worklist is what the quantitative pipeline could not decide on its own. "
        "Read each skill's SKILL.md and answer the three questions at the bottom. "
        "Append your findings to `research/findings/{date}.md` before the human reviews.\n"
    )
    lines.append("## Reading instructions\n")
    lines.append(
        "For each skill below, open its `SKILL.md` in `/tmp/clawhub-skills/skills/<owner>/<slug>/SKILL.md` "
        "(or fetch from [github.com/openclaw/skills](https://github.com/openclaw/skills)). "
        "Do **not** rely on the description or the auto-extracted pattern hits — read the actual body. "
        "Reading is the point; pattern hits are a hint, not a substitute.\n"
    )

    lines.append("---\n")
    lines.append(
        f"## 1. Top {len(groups['top'])} by downloads (reference class)\n"
    )
    lines.append("_These are the most-downloaded skills. Any structural move they make is high-leverage. Read them first._\n")
    for s in groups["top"]:
        lines.append(_worklist_row(s))

    lines.append("")
    lines.append(
        f"## 2. New entrants into top {THRESHOLDS['new_top20_threshold']} ({len(groups['new_entrants'])} skills)\n"
    )
    lines.append("_Skills that weren't in the previous snapshot's top 20. Check whether they invent something new._\n")
    if groups["new_entrants"]:
        for s in groups["new_entrants"]:
            lines.append(_worklist_row(s))
    else:
        lines.append("_None this cycle._\n")

    lines.append("")
    lines.append(f"## 3. Structural outliers ({len(groups['outliers'])} skills)\n")
    lines.append(
        "_Skills whose shape (lines/sections/code blocks/scripts) is unusual among the top 1,000 and whose regex pattern hits are below average. These are the most likely candidates to be using a pattern the detectors don't know about._\n"
    )
    if groups["outliers"]:
        for s in groups["outliers"]:
            lines.append(_worklist_row(s))
    else:
        lines.append("_None this cycle._\n")

    lines.append("")
    lines.append("## 4. Pattern candidates (quantitative hint)\n")
    if diff.pattern_candidates:
        lines.append(
            "_The regex pipeline says these known patterns are rising but haven't hit threshold. "
            "Read a handful of skills in the top 20 that match each pattern to verify the detector isn't over-counting._\n"
        )
        for name, cnt in diff.pattern_candidates:
            lines.append(f"- `{name}`: {cnt} skills in top 20 (need ≥{THRESHOLDS['pattern_add_min']})")
    else:
        lines.append("_No candidates near threshold this cycle._\n")

    lines.append("")
    lines.append("## 5. Broken citations (auto-detected — verify, don't trust)\n")
    # Broken citations are filled in at the call site; this section is a placeholder
    # the caller injects into.
    lines.append("_See `research/reports/{date}.md` for the citation validation results. Each broken citation needs a human or agent decision: replace with an equivalent skill, or rework the paragraph to not need the citation._\n")

    lines.append("---\n")
    lines.append("## Questions to answer per skill\n")
    lines.append(
        "For each skill you read (especially in Sections 2 and 3), write a brief note answering:\n\n"
        "1. **Is there a structural pattern here that is NOT in `book/04-skill-patterns.md`?** "
        "If yes, describe it in one sentence. If 3+ skills in this worklist share it, it's a candidate for `research/candidates.md`. "
        "If 5+ skills across the full top 1,000 share it (check by reading more widely), propose a new pattern entry.\n\n"
        "2. **Does this skill quote or declare a design stance worth adding to `book/01-philosophy.md`?** "
        "Only if a higher-downloaded skill makes a principle's point better than the current citation does. "
        "Do not add a principle based on a single skill.\n\n"
        "3. **If this skill is cited in the book, are the citation's specifics still accurate?** "
        "Check the quoted text still appears in SKILL.md verbatim, and the download count cited matches current data (±5%).\n\n"
        "## Non-findings are findings\n\n"
        "If you read the whole worklist and nothing in the book needs to change, write that down. "
        "A flat cycle is a valid cycle. The changelog should record it.\n"
    )
    return "\n".join(lines)


def _worklist_row(s: Skill) -> str:
    hit_count = sum(1 for v in s.pattern_hits.values() if v)
    scripts_info = f"{s.script_count} scripts" if s.has_scripts else "no scripts"
    refs_info = f"{s.ref_count} refs" if s.has_refs else "no refs"
    return (
        f"- [`{s.slug}`](https://clawhub.ai/skills/{s.slug}) — "
        f"{s.downloads:,} dl · {s.lines} lines · {s.sections} sections · "
        f"{s.code_blocks} code blocks · {scripts_info} · {refs_info} · "
        f"{hit_count} known patterns hit"
    )


def save_worklist(text: str, snap_date: str) -> Path:
    WORKLISTS_DIR.mkdir(parents=True, exist_ok=True)
    path = WORKLISTS_DIR / f"{snap_date}.md"
    path.write_text(text)
    return path


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


def cmd_worklist(_: argparse.Namespace) -> int:
    """Emit an agent-facing worklist based on the latest snapshot."""
    snapshots = sorted(SNAPSHOTS_DIR.glob("*.json")) if SNAPSHOTS_DIR.exists() else []
    if not snapshots:
        die("no snapshot exists — run `research.py fetch` first")
    snap = load_latest_snapshot()
    prev = load_latest_snapshot(exclude=snapshots[-1]) if len(snapshots) >= 2 else None
    diff = diff_snapshots(snap, prev)
    groups = build_worklist(snap, diff)
    text = render_worklist(snap, groups, diff)
    path = save_worklist(text, snap.date)
    log(f"worklist: {path.relative_to(REPO_ROOT)}")
    print(text)
    return 0


def cmd_default(_: argparse.Namespace) -> int:
    """Full pipeline: fetch, analyze, compare, validate, then build worklist."""
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

    worklist = render_worklist(snap, build_worklist(snap, diff), diff)
    worklist_path = save_worklist(worklist, snap.date)
    log(f"worklist: {worklist_path.relative_to(REPO_ROOT)}")

    log("pipeline complete — next step: an agent reads the worklist, not the report")
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
        "worklist": cmd_worklist,
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
