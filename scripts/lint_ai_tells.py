#!/usr/bin/env python3
"""Flag common signs of AI-generated writing.

Patterns come from Wikipedia's "Wikipedia:Signs of AI writing" (November 2026).
Standard library only.

Usage:
  python lint_ai_tells.py FILE [FILE ...]
  python lint_ai_tells.py - < draft.txt
  python lint_ai_tells.py --json FILE
  python lint_ai_tells.py --min-severity medium FILE

Exit status: 1 if any high-severity hit is found, 2 on usage errors, else 0.
Prose checks skip fenced code blocks; artifact, placeholder, tracking and
punctuation checks run everywhere.
"""

import argparse
import json
import re
import statistics
import sys

HIGH, MED, LOW = "high", "medium", "low"
RANK = {LOW: 0, MED: 1, HIGH: 2}


def words(*items):
    return r"\b(?:" + "|".join(items) + r")\b"


# (category, severity, pattern, hint, scope) where scope is "all" or "prose"
RULES = [
    # Punctuation
    ("em dash", HIGH, r"—", "use a comma, colon, parentheses, or a new sentence", "all"),
    ("spaced en dash", MED, r"(?<=\w) – (?=\w)", "used as a dash; rewrite the punctuation", "all"),
    ("curly quote", MED, r"[“”‘’]", "use straight quotes", "all"),
    ("emoji", MED, r"[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF☀-➿⭐⭕]", "remove unless the user wants emoji", "all"),

    # Leaked tool artifacts and tracking
    ("tool artifact", HIGH, r"contentReference|oaicite|citeturn\w*|turn\d+search\d+|↩", "leaked chatbot citation markup; remove", "all"),
    ("tracking param", HIGH, r"utm_source=(?:chatgpt\.com|openai|copilot\.com)|referrer=grok\.com", "strip the tracking parameter", "all"),

    # Placeholders
    ("placeholder", HIGH, r"\[(?:(?:[A-Z][\w']{0,20} ){0,3}(?:Name|Year|Date|Title|Company|City|URL|Link|Here|Number)|Insert[^\]]*|Your [^\]]*|Add [^\]]*|TBD|TODO)\]", "fill in or remove", "all"),
    ("placeholder", HIGH, r"\b(?:19|20)\d\d-[Xx]{2}-[Xx]{2}\b", "placeholder date", "all"),
    ("placeholder", HIGH, r"\bINSERT_[A-Z_#0-9]+\b", "placeholder URL", "all"),
    ("placeholder", HIGH, r"\((?:Add|Insert)[^)]*here\)|\(If available\)|<!--\s*Add if available[^>]*-->", "fill in or remove", "all"),
    ("placeholder", MED, r"\bexample\.com/\w+", "placeholder link", "all"),
    ("placeholder text", HIGH, r"\[(?:tag|insert|add|your|link|name|names|todo|tbd|placeholder|company|date|url|teammates?|team member|person|role)\b[^\]\n]{0,40}\](?!\()", "fill in or remove; tell the user what's missing outside the text", "all"),

    # Chatbot packaging and boilerplate
    ("chatbot filler", HIGH, r"\b(?:Certainly|Of course|Absolutely)!|\bGreat question\b|\byou'?re absolutely right\b|\bI hope this helps\b|\bis there anything else\b", "delete; start with the answer", "prose"),
    ("chatbot filler", MED, r"\blet me know if\b|\bwould you like (?:me )?to\b|\bfeel free to\b|\bmore detailed breakdown\b|\bhappy to help\b|\ba Wikipedia-style article\b", "delete the offer", "prose"),
    ("chatbot filler", LOW, r"^\s*here(?: is|'s) (?:a|an|the|your)\b", "consider starting with the content itself", "prose"),
    ("AI boilerplate", HIGH, r"\bas an AI(?: language model)?\b|\bas a large language model\b|\bas of my (?:last )?(?:knowledge|training) (?:update|cutoff)\b|\bup to my last training update\b", "never include", "prose"),
    ("customer-service tone", MED, r"\bI have carefully reviewed\b|\bapolog\w* for any inconvenience\b|\bI hope this (?:message|email) finds you well\b|\bI trust this message finds you well\b|\bI am writing to\b|\bI understand your concerns\b|\bDear [\w ]{0,30}Team\b", "write plainly in your own voice", "prose"),

    # Hedging disclaimers
    ("hedging disclaimer", MED, r"\b(?:specific )?details (?:are|remain) (?:limited|scarce)\b|\bnot widely (?:available|documented|disclosed|reported)\b|\bbased on (?:the )?available information\b|\bin the (?:provided|available) (?:sources|search results|information)\b|\bdoes not by itself establish\b|\bshould (?:be treated|be presented|be read) as\b|\bshould not be confused with\b|\bit(?: is|'s) (?:important|worth) (?:to note|noting)\b|\bmaintains? a low profile\b|\bkeeps? (?:personal|private) (?:details|life) private\b", "say once that it's unknown, or cut", "prose"),

    # Significance and legacy
    ("inflated significance", MED, r"\b(?:stands?|serves?) as (?:a|an)\b(?: \w+){0,3} (?:testament|reminder|symbol|beacon|example)\b|\b(?:is|are|was|remains) a testament\b|\ba testament to\b|\b(?:crucial|pivotal|vital|significant|key|instrumental) (?:role|moment|part)\b|\b(?:underscor|highlight|emphasiz)\w* (?:its|the|their|his|her) (?:importance|significance)\b|\breflects? (?:the )?broader\b|\bsymboliz\w* (?:its|the|their) (?:ongoing|enduring|lasting)\b|\bsetting the stage for\b|\b(?:marks?|represents?|marking|representing) a (?:shift|turning point|milestone)\b|\bkey turning point\b|\bevolving landscape\b|\bfocal point\b|\bindelible mark\b|\bdeeply rooted\b|\b(?:this|that|it|which) matters\b|\bmatters because\b|\bwhy (?:this|it) matters\b", "give the specific fact instead", "prose"),
    ("notability emphasis", MED, r"\bindependent coverage\b|\b(?:local|regional|national|international) media outlets?\b|\btrade publications?\b|\b(?:has been |was )?(?:profiled|featured) in\b|\bleading expert\b|\bactive social media presence\b", "report what sources said, not that they exist", "prose"),
    ("identification emphasis", MED, r"\b(?:identif(?:y|ies)|lists?|describes?) (?:him|her|them|it) as\b|\b(?:was|is|were) identified (?:by|as)\b|\bprofessional profile lists\b", "state the fact and cite it", "prose"),
    ("superficial -ing clause", MED, r",\s(?:highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|contributing to|cultivating|fostering|encompassing|enhancing|showcasing|solidifying|cementing|reinforcing)\b", "end the sentence at the fact", "prose"),
    ("superficial analysis", MED, r"\bvaluable insights?\b|\b(?:aligns?|resonates?|resonating|aligning) with\b", "cut or make concrete", "prose"),
    ("vague association", MED, r"\bin connection (?:with|to)\b|\bconnected (?:with|to)\b|\bin association with\b|\b(?:closely |widely |particularly )?associated with\b", "state the actual relationship", "prose"),
    ("vague attribution", MED, r"\bindustry reports\b|\bobservers (?:have )?(?:cited|noted|say)\b|\bexperts (?:argue|say|note|agree|believe)\b|\b(?:some )?critics (?:argue|have noted|say)\b|\bseveral (?:sources|publications|reviewers|scholars)\b|\bit is widely (?:believed|regarded|considered)\b", "name the source, or drop it", "prose"),
    ("challenges formula", MED, r"\bdespite (?:its|these|their|his|her)\b[^.\n]{0,80}\bchallenges\b|\bfaces? (?:several |many |numerous |significant )?challenges\b|\bfuture (?:outlook|prospects)\b|\bdespite these challenges\b", "drop the formula; give specifics in place", "prose"),
    ("summary phrase", MED, r"(?:^|[.!?]\s+)(?:In summary|In conclusion|Overall|To sum up|Ultimately),", "cut the recap", "prose"),

    # Copula avoidance
    ("copula avoidance", MED, r"\b(?:serves?|stands?|functions?|operates?) as (?:a|an|the)\b", "use is/are", "prose"),
    ("copula avoidance", LOW, r"\b(?:boasts?|features|offers) (?:a|an)\b|\bholds the distinction of\b|\brefers to\b", "consider is/has", "prose"),

    # Negative parallelisms
    ("negative parallelism", MED, r"\bnot only\b[^.!?\n]{1,120}?\bbut\b", "state the point directly", "prose"),
    ("negative parallelism", MED, r"\bnot just\b[^.!?\n]{1,120}?\b(?:but|it'?s|they'?re)\b", "state the point directly", "prose"),
    ("negative parallelism", MED, r"\b(?:it'?s|it is|this is|that'?s|this isn'?t|it isn'?t) not\b[^.!?\n]{1,80}?[,;:]\s*(?:it'?s|it is|this is|that'?s|but)\b|\b(?:it|this|that) isn'?t (?:about )?\w+[^.!?\n]{0,60}?[,;:]\s*(?:it'?s|it is)\b", "state the point directly", "prose"),
    ("negative parallelism", MED, r"\bno \w+(?: \w+)?, no \w+(?: \w+)?,? (?:just|only)\b", "state the point directly", "prose"),
    ("negative parallelism", LOW, r"\brather than\b", "check it isn't a 'Y rather than X' flourish", "prose"),

    # Promotional language
    ("promotional", MED, r"\bnestled\b|\bin the heart of\b|\bgroundbreaking\b|\brenowned\b|\bcommitment to\b|\bnatural beauty\b|\bdiverse array\b|\brich (?:history|heritage|tradition|culture|tapestry)\b|\bprofound\b|\bexemplif\w+\b|\bseamless(?:ly)?\b|\bcutting-edge\b|\bgame-?changer\b|\bunparalleled\b|\bbreathtaking\b|\bstunning\b", "neutral description with facts", "prose"),

    # Edit summaries, commit messages, PR descriptions
    ("canned change summary", MED, r"\bimprov\w* (?:the )?(?:clarity|flow|readability|maintainability|robustness)\b|\b(?:enhanc|refin)\w* (?:the )?(?:tone|clarity|readability|flow)\b|\bensur\w* (?:compliance|neutrality|consistency)\b|\bin compliance with\b|\bcomplies with\b|\b(?:encyclopedic|neutral) tone\b|\bwhile (?:preserving|retaining|maintaining) (?:the )?(?:existing|original)\b|\b(?:preserved|retained) (?:the )?(?:existing|original)\b|\badded (?:sourced|verified) (?:information|content)\b|\baddress(?:ed|ing) (?:the )?reviewer(?:'s)? feedback\b|\bstreamlin\w+\b", "say concretely what changed", "prose"),

    # AI vocabulary
    ("AI vocabulary", MED, words(
        "additionally", "boasts?", "boasting", "bolster(?:s|ed|ing)?", "crucial(?:ly)?",
        "delv(?:e|es|ed|ing)", "deep dive", "emphasiz(?:e|es|ed|ing)", "enduring",
        "enhanc(?:e|es|ed|ing|ement)", "foster(?:s|ed|ing)?", "garner(?:s|ed|ing)?",
        "highlight(?:s|ed|ing)?", "interplay", "intricate(?:ly)?", "intricac(?:y|ies)",
        "meticulous(?:ly)?", "pivotal", "showcas(?:e|es|ed|ing)", "tapestry",
        "testament", "underscor(?:e|es|ed|ing)", "vibrant", "align(?:s|ed)? with",
        "leverag(?:e|es|ed|ing)", "multifaceted", "prioritiz(?:e|es|ed|ing)",
        "navigat(?:e|es|ing) the (?:complexities|landscape)", "realm", "embark(?:s|ed|ing)?",
        "invaluable", "holistic", "synerg(?:y|ies)", "paramount"),
     "use the plain word, or cut", "prose"),
    ("AI vocabulary", LOW, words(
        "valuable", "robust(?:ly|ness)?", "landscape", "quietly", "steady", "dependable",
        "universally", "echoed", "causal", "empirical(?:ly)?", "correlat(?:e|es|ed)",
        "notably", "moreover", "furthermore", "comprehensive"),
     "fine if literal; otherwise use a plainer word", "prose"),
]

# Placeholders and summary openers are matched case-sensitively so ordinary
# lowercase prose ("[your name]" aside) doesn't trip them.
CASE_SENSITIVE = {"placeholder", "summary phrase"}
COMPILED = [
    (c, s, re.compile(p, re.MULTILINE if c in CASE_SENSITIVE else re.IGNORECASE | re.MULTILINE), h, sc)
    for c, s, p, h, sc in RULES
]

MINOR = {"a", "an", "the", "and", "or", "but", "nor", "for", "so", "yet", "as", "at",
         "by", "in", "of", "on", "to", "up", "via", "with", "from", "into", "over", "per"}
ATTRIBUTION_RX = re.compile(r"Generated with \[Claude Code\]|^Co-Authored-By:", re.IGNORECASE)
HEADING_RX = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
INLINE_HEADER_RX = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\*\*[^*]+\*\*\s*:?")
BOLD_RX = re.compile(r"\*\*[^*\n]+\*\*|__[^_\n]+__")
FORMULA_HEADINGS = re.compile(
    r"^(?:conclusion|in conclusion|summary|challenges(?: and \w+)?|future (?:outlook|prospects|directions)|"
    r"awards and recognition|recognition|legacy and impact|impact and legacy)$", re.IGNORECASE)


# Checks that describe a whole line or file; they never hide or get hidden by span hits.
WHOLE_LINE = {"uniform sentence length", "heavy bold", "inline-header list",
              "title case heading", "formula heading"}


def hit(line_no, col, sev, cat, text, hint):
    return {"line": line_no, "col": col, "severity": sev, "category": cat, "match": text, "hint": hint}


def check_heading(line_no, title):
    out = []
    plain = re.sub(r"[*_`]", "", title).strip()
    if FORMULA_HEADINGS.match(plain):
        out.append(hit(line_no, 1, MED, "formula heading", plain, "fold into the body or use a specific heading"))
    tokens = re.findall(r"[A-Za-z][A-Za-z'\-]*", plain)
    rest = [t for t in tokens[1:] if t.lower() not in MINOR and not t.isupper()]
    caps = [t for t in rest if t[0].isupper()]
    if len(rest) >= 2 and len(caps) == len(rest):
        out.append(hit(line_no, 1, MED, "title case heading", plain, "use sentence case"))
    return out


def lint_text(text):
    hits = []
    lines = text.splitlines()
    in_fence = False
    prose_chunks = []  # (line_no, text) for sentence-length analysis
    inline_headers = []
    bold_count = 0
    prose_words = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if ATTRIBUTION_RX.search(line):
            continue  # required tool attribution lines are not the author's prose

        for cat, sev, rx, hint, scope in COMPILED:
            if scope == "prose" and in_fence:
                continue
            for m in rx.finditer(line):
                hits.append(hit(i, m.start() + 1, sev, cat, m.group(0), hint))

        if in_fence:
            continue

        h = HEADING_RX.match(line)
        if h:
            hits.extend(check_heading(i, h.group(2)))
            continue
        if INLINE_HEADER_RX.match(line):
            inline_headers.append(i)
        bold_count += len(BOLD_RX.findall(line))
        if stripped and not re.match(r"^\s*(?:[-*+>|]|\d+[.)])\s", line):
            prose_chunks.append((i, stripped))
            prose_words += len(stripped.split())

    if len(inline_headers) >= 3:
        hits.append(hit(inline_headers[0], 1, LOW, "inline-header list",
                        f"{len(inline_headers)} bullets start with a bold label",
                        "consider prose or a plain list"))
    if bold_count >= 3 and prose_words and bold_count / max(prose_words, 1) > 1 / 120:
        hits.append(hit(1, 1, LOW, "heavy bold",
                        f"{bold_count} bold spans in about {prose_words} words of prose",
                        "bold almost nothing in running text"))

    # Uniform sentence length (a newer sign once em dashes were suppressed)
    joined = " ".join(t for _, t in prose_chunks)
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", joined) if len(s.split()) >= 3]
    if len(sentences) >= 8:
        lengths = [len(s.split()) for s in sentences]
        in_band = sum(8 <= n <= 20 for n in lengths) / len(lengths)
        spread = statistics.pstdev(lengths)
        if in_band >= 0.85 and spread < 4.5:
            hits.append(hit(prose_chunks[0][0], 1, LOW, "uniform sentence length",
                            f"{in_band:.0%} of {len(lengths)} sentences are 8-20 words (stdev {spread:.1f})",
                            "vary sentence length and punctuation"))

    # Drop duplicates where a weaker hit overlaps a stronger one on the same span
    hits.sort(key=lambda x: (x["line"], x["col"], -RANK[x["severity"]]))
    kept, spans = [], {}
    for x in hits:
        start, end = x["col"], x["col"] + len(x["match"])
        taken = spans.setdefault(x["line"], [])
        if x["category"] in WHOLE_LINE:
            kept.append(x)
            continue
        if any(start < e and s < end for s, e in taken):
            continue
        taken.append((start, end))
        kept.append(x)
    return kept


def main(argv=None):
    ap = argparse.ArgumentParser(description="Flag signs of AI-generated writing.")
    ap.add_argument("files", nargs="+", help="files to check, or - for stdin")
    ap.add_argument("--json", action="store_true", help="print JSON")
    ap.add_argument("--min-severity", choices=[LOW, MED, HIGH], default=LOW)
    args = ap.parse_args(argv)

    floor = RANK[args.min_severity]
    report = {}
    for f in args.files:
        if f == "-":
            text, name = sys.stdin.read(), "<stdin>"
        else:
            try:
                with open(f, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError as e:
                print(f"error: {e}", file=sys.stderr)
                return 2
            name = f
        report[name] = [x for x in lint_text(text) if RANK[x["severity"]] >= floor]

    any_high = any(x["severity"] == HIGH for hits in report.values() for x in hits)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if any_high else 0

    total = {HIGH: 0, MED: 0, LOW: 0}
    for name, hits in report.items():
        for x in hits:
            total[x["severity"]] += 1
            print(f"{name}:{x['line']}:{x['col']}  {x['severity']:<6} {x['category']}: "
                  f"{x['match']!r}  ({x['hint']})")
    n = sum(total.values())
    print(f"\n{n} hit(s): {total[HIGH]} high, {total[MED]} medium, {total[LOW]} low")
    return 1 if any_high else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
