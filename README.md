# avoid-ai-tells

A Claude skill that keeps writing from reading as AI-generated. It is built from Wikipedia's advice page [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and gives Claude three things: the core rules and the reasons for them, a catalog of all 47 patterns the page lists, and a linter that flags them line by line.

It applies to anything Claude writes for people to read: chat answers, emails, posts, docs, READMEs, code comments, commit messages and PR descriptions. It also covers requests like "humanize this" or "does this sound like AI?".

From AI Hustle World (AHW).

## What it changes

Most AI tells are easy to see once you know them: "delve", "pivotal", "a testament to", "not just X, it's Y", em dashes, title-case headings, bolded bullet labels, "I hope this helps!". The skill tells Claude to drop those and use plain words.

The bigger change is about content. The Wikipedia page points out that the wording is a symptom: AI text swaps specific facts for generic, inflated claims. So the skill also tells Claude to:

- use only the facts it was given, and ask for a real detail instead of making one up
- leave no placeholders like `[tag teammates]` in finished text
- keep caveats and risks while cutting filler
- avoid overcorrecting into flat text made only of commas and periods

## Does it help?

We ran 5 writing tasks (a LinkedIn rewrite, a README, a commit message and PR, a bakery "About us" page, a promotion post), twice each with the skill and twice without it, and graded every output against the same checks.

| | With the skill | Without it |
|---|---|---|
| Checks passed | 98 of 100 | 86 of 100 |
| Runs that stated facts the user never gave | 1 of 10 | 8 of 10 |
| Leftover placeholders | 0 | 1 |

Without the skill, Claude invented product descriptions, anecdotes, feelings and undocumented tool behavior. With it, Claude stuck to what it was told and listed what was missing. Both configurations already avoided most surface tells, so the difference is mostly in made-up content.

This is a small test, and the invented-facts check was judged by hand by the person who wrote the skill. Treat the numbers as a sign, not proof.

## Install

**Claude Code.** Clone the repo into your skills folder:

```bash
git clone https://github.com/Muntasir-11/ahw-avoid-ai-tells ~/.claude/skills/avoid-ai-tells
```

**Claude.ai.** Download `avoid-ai-tells.skill` from this repo and add it in your Claude skills settings.

## The linter

`scripts/lint_ai_tells.py` needs only Python 3 and its standard library.

```bash
python scripts/lint_ai_tells.py draft.md
python scripts/lint_ai_tells.py - < draft.txt
python scripts/lint_ai_tells.py --json --min-severity medium draft.md
```

Each hit has a line, column, severity and a fix hint. The exit status is 1 when it finds a high-severity hit (em dashes, chatbot filler, placeholders, leaked citation markup, tracking parameters), so you can use it in a pre-commit hook or CI. It is a net, not a judge: some hits are fine in context, and some tells (invented facts, inflated claims in fresh words) need a human read.

## Files

- `SKILL.md`: the instructions Claude follows
- `references/patterns.md`: all 47 patterns in 8 groups, with words to watch and fixes, plus the signs of human writing worth keeping
- `scripts/lint_ai_tells.py`: the linter
- `avoid-ai-tells.skill`: the same skill packaged for claude.ai

## Source and license

The patterns are summarized in our own words from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) by WikiProject AI Cleanup, read in November 2026. Wikipedia text is available under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The page describes AI writing on Wikipedia; this skill turns its observations into writing rules, so mistakes in that translation are ours.

The code and the rest of this repo are under the MIT License. See [LICENSE](LICENSE).
