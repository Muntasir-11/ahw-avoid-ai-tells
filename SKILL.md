---
name: avoid-ai-tells
description: Write and edit text so it does not read as AI-generated, using the full catalog of tells from Wikipedia's "Signs of AI writing" page plus a bundled linter that flags them line by line. Use this whenever you write or revise prose that someone will read, such as chat answers, emails, posts, articles, reports, documents, READMEs, code comments, docstrings, commit messages, PR descriptions, changelogs, or edit summaries. Also use it when the user asks to humanize or de-slop a draft, asks "does this sound like AI", wants AI tells or em dashes removed, or wants a draft checked before it is sent or published, even if they never say "AI".
---

# Avoid AI tells

Language models drift toward the most statistically likely wording. In practice that means specific facts get replaced by generic, inflated claims ("inventor of the first train-coupling device" becomes "a revolutionary titan of industry"), and a small set of words, sentence shapes and formatting habits shows up far more often than in human writing. Readers who have seen a lot of AI text notice these within a sentence or two, and once they do, they stop trusting the rest.

This skill is built from Wikipedia's advice page "Wikipedia:Signs of AI writing" (WikiProject AI Cleanup, read November 2026). That page describes what AI text looks like. This skill turns it into rules for writing text that doesn't look like that.

## Files

- `references/patterns.md`: the complete catalog, 47 patterns in 8 groups, each with words to watch and how to fix it. Read it when reviewing someone else's draft, when a linter hit is unclear, or when writing a long or public piece.
- `scripts/lint_ai_tells.py`: a standard-library Python linter. It reports each hit with line, column, severity and a fix hint.

## Workflow

**Writing something new.** Keep the core rules below in mind while drafting. For anything longer than a few sentences, or anything that will be sent, published or committed, save the draft to a temporary file and run the linter on the finished draft. Fix the hits, then reread the whole thing once for the problems a regex can't see (inflated claims phrased in fresh words, invented facts, padding). Run the linter again only if you changed a lot; each run costs time, and running it after every small edit makes the task several times slower without improving the text.

**Reviewing or humanizing the user's text.** Run the linter on the original first so you have a concrete list. Then rewrite and lint the result once. Afterwards, tell the user in a few lines what kinds of things you changed. Don't list every word.

**Only use facts you were given.** When rewriting or drafting from someone's notes, it is tempting to add a vivid specific ("we sat in on research sessions") to make the text sound human. That is inventing, and it is worse than any AI tell because the person may publish it. Keep to the facts in the source. If one real detail would make the text better, say so in your message to the user, outside the deliverable. The same goes for docs: don't state behavior the user didn't describe (file formats, which duplicate keeps the plain name, defaults). Leave it out, and list your open questions in your reply.

**No placeholders in finished text.** Don't leave "[tag teammates]" or "[your name]" for the user to fill in. Write the text so it works without them, and mention in your reply what they might add.

```bash
python scripts/lint_ai_tells.py draft.md          # one or more files
python scripts/lint_ai_tells.py - < draft.txt     # stdin
python scripts/lint_ai_tells.py --json draft.md   # machine-readable
python scripts/lint_ai_tells.py --min-severity medium draft.md
```

It exits with status 1 when it finds a high-severity hit. Severities: `high` is almost always wrong (em dashes, chatbot filler, placeholders, leaked tool artifacts, tracking parameters); `medium` is usually wrong (AI vocabulary, stock phrases, negative parallelisms); `low` depends on context ("rather than", "refers to", "landscape", uniform sentence length).

Treat the linter as a net, not a judge. Some hits are fine in context: "features" in a software changelog, "robust" in statistics, "landscape" for actual terrain, "highlight" as a noun. And some tells it can't catch at all, so the reread matters.

## Core rules

These cover most of what readers notice. The full list with examples is in `references/patterns.md`.

1. **Say the specific thing.** Don't tell readers something is important, pivotal, a testament, or part of a broader trend. Give the fact that would make them conclude it themselves. If you don't have that fact, cut the sentence or ask; don't make one up.
2. **Skip the AI vocabulary.** delve, tapestry, testament, pivotal, crucial, underscore, highlight (verb), showcase, foster, enhance, garner, intricate, meticulous, vibrant, boasts, bolstered, interplay, align with, enduring, additionally (opening a sentence), leverage, multifaceted, seamless, robust. Use the plain word, or nothing.
3. **Use "is", "are" and "has".** Not "serves as", "stands as", "functions as", "features", "offers", "boasts".
4. **No negative parallelisms.** "Not just X, but Y", "It's not X, it's Y", "no X, no Y, just Z". State Y.
5. **No reflexive threes.** Three adjectives or three parallel phrases in a row reads as padding. Use the number of items you actually have.
6. **No tacked-on "-ing" commentary.** Sentences that end in ", highlighting its...", ", ensuring...", ", reflecting..." are adding analysis nobody asked for. End the sentence at the fact.
7. **No vague attribution.** "Experts say", "observers note", "several sources" with one source. Name who said it or drop it.
8. **No chatbot packaging.** No "Certainly!", "Great question", "I hope this helps", "Let me know if...", "Would you like me to...". Start with the answer and stop when it's done.
9. **No hedges about sources.** "Details are limited", "based on available information", "should be treated as X rather than Y". If something is unknown, say so once, plainly.
10. **Punctuation and format.** No em dashes. Straight quotes. Sentence-case headings. No emoji unless asked. Bold sparingly. Prose over bulleted "**Label:** text" lists when prose works.
11. **No placeholders or invented citations.** No [Name], 2025-XX-XX, example.com/source1. Never fabricate a link, DOI, ISBN or page number.

## Fix the content, not only the wording

The Wikipedia page warns that these signs point to deeper problems, and that cleaning up the surface only makes those problems harder to see. "The festival plays a pivotal role in the region's evolving cultural landscape" doesn't get better with synonyms. Either find the fact behind it ("About 40,000 people attend each August, roughly the town's population") or delete it.

## Cut padding, not substance

Plain writing is shorter, but the goal is to remove filler, not information. Keep caveats, risks, side effects, limitations and anything else the reader needs in order to act. A PR description that drops "retries resend the whole upload, so check the endpoint is idempotent" is worse, even if every remaining sentence is clean. Say those things plainly; don't delete them.

## Don't overcorrect

Newer models that were trained never to use em dashes now produce text made only of commas and periods, in sentences that all run 8 to 20 words. That flatness has become a tell of its own. So when you remove a dash, choose whatever fits: a colon, parentheses, a semicolon, a new sentence, or a rewrite. Let sentence length vary.

The page also lists what human writing tends to have, and these are worth keeping:

- plain "is" and "has" ("there is a", "it has a")
- plain verbs: wrote, moved, used, tried, died (not authored, relocated, utilized, attempted, passed away)
- superlatives and definite claims when they are true ("was the first", "is the only")
- qualifiers and intensifiers ("very", "perhaps", "tends to")
- ordinary wordy phrases ("as a result of", "the fact that")

Repeating the right word is fine. Swapping in a new synonym each time ("the artist... the painter... the creator") is an AI habit.

## By context

- **Chat replies.** Answer first. No opener praising the question, no closing offer of more help, no recap of what you just said.
- **Documents and articles.** No "Challenges" or "Future outlook" sections built on a formula, no "Conclusion" that restates the body, no "Awards and recognition" heading by reflex. Headings in sentence case.
- **Commit messages, PR descriptions, edit summaries.** Say what changed and why, concretely: "Fix off-by-one in pagination when page size is 1". Not "Improved clarity, robustness and maintainability while preserving existing behavior". Don't list what you didn't change, don't claim compliance with guidelines, don't itemize parameter names. Do include what a reviewer should watch for (risks, behavior changes). Attribution lines the tool requires (Co-Authored-By, "Generated with Claude Code") stay as they are, emoji included; the linter skips them.
- **Code comments and docstrings.** Say what something does or why it exists, briefly. No "This robust utility seamlessly handles...". Don't restate the code.
- **Citations and links.** Only cite what you have checked. Strip `utm_source=chatgpt.com` and similar parameters. Never leave `contentReference`, `oaicite` or ↩ artifacts.

## Examples

**Prose**

Before: "Nestled in the heart of the valley, the town serves as a vibrant testament to the region's rich heritage, showcasing its enduring cultural significance."

After: "The town sits on the valley floor. It has a 12th-century church and a market that has run every Saturday since 1290."

The second version needs real facts. If you don't have them, ask the user or say less.

**Commit message**

Before: "Enhanced the authentication module to ensure robust error handling, improving clarity and maintainability while preserving existing functionality."

After: "Return 401 instead of 500 when the session token is expired"

**Chat reply**

Before: "Great question! Python's GIL is not just a lock, it's a fundamental design choice that shapes concurrency. I hope this helps! Let me know if you'd like a deeper dive."

After: "The GIL lets only one thread run Python bytecode at a time, so threads won't speed up CPU-bound code. Use multiprocessing for that, or threads for I/O-bound work."
