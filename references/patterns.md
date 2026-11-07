# Pattern catalog

Every pattern from Wikipedia's "Wikipedia:Signs of AI writing" (read November 2026), in the page's own grouping, rewritten as things to avoid. Each entry has what it looks like, words to watch where the page gives them, and the fix. The page is a field guide for spotting AI text on Wikipedia, so a few entries (AfC drafts, user pages) are Wikipedia-specific; they are kept because the habit behind them shows up elsewhere too.

Contents

1. Content (1 to 8)
2. Language and grammar (9 to 14)
3. Style (15 to 20)
4. Text addressed to the user (21 to 23)
5. Markup and citations (24 to 30)
6. Comments and edit summaries (31 to 33)
7. Miscellaneous (34 to 39)
8. Older signs, mostly 2022 to 2025 (40 to 47)
9. Signs of human writing (what to keep)
10. Signs that are not reliable

---

## 1. Content

### 1. Inflated significance, legacy and broader trends
Arbitrary details get framed as part of something bigger. Even etymology or population figures get a line about their importance, sometimes after a hedge admitting the topic is minor. Biology text over-stresses ecosystem links and conservation efforts that may not exist. Newer models pair this with editorializing about why "this distinction matters".
Watch: stands/serves as, is a testament/reminder, a crucial/pivotal/vital/significant/key role or moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted, "[distinction] matters because", situating the subject amid "debates" or "public discussions".
Fix: give the concrete fact or cut the sentence.

### 2. Canned emphasis on notability, attribution and media coverage
Proving importance by listing the kinds of outlets that covered the subject instead of saying what they reported. Often echoes guideline language ("independent coverage").
Watch: independent coverage, local/regional/national media outlets, music/business/tech outlets, trade publications, cited/featured/profiled in, written by a leading expert, active social media presence.
Fix: report what the source said, attributed to the source by name.

### 3. Undue emphasis on identification by primary or tertiary sources
Stilted statements about how a database, record, filing or profile "identifies" the subject. Common from 2026.
Watch: records/listings/filings identify/list/describe X as, was identified by [source] as, is listed in, his/her professional profile lists.
Fix: state the fact and cite the source.

### 4. Superficial analysis
A present-participle clause added to the end of a sentence to comment on significance or impact, sometimes pinned on a named source that never said it.
Watch: highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, cultivating, fostering, encompassing, enhancing, valuable insights, align/resonate with.
Fix: end the sentence at the fact. If the analysis is real and sourced, give it its own sentence with attribution.

### 5. Vague expression of connection or association
Saying two things are "connected" or "associated" instead of stating the relationship.
Watch: in connection with/to, connected with/to, in association with, associated with, particularly/widely associated.
Fix: "was CEO of", "taught chemistry at", "founded".

### 6. Vague attributions and overgeneralized opinions
Weasel wording, and stretching one or two sources into a consensus. Implying a list is a sample when it is the whole set.
Watch: industry reports, observers have cited, experts argue, some critics argue, several sources/publications (when few are cited), "such as" before a complete list.
Fix: name the person or publication. Say "two reviewers" if there are two.

### 7. Outline-like conclusions about challenges and future prospects
A closing "Challenges" section that opens "Despite its [praise], X faces challenges..." and ends on vague optimism or speculation, often followed by "Future prospects". The problem is the formula, not mentioning difficulties.
Watch: Despite its... faces several challenges, Despite these challenges, Challenges and legacy, Future outlook.
Fix: put real problems where they belong in the narrative, with specifics. Drop the speculative ending.

### 8. "Awards and recognition" sections
Headings in "X and Y" form in general, and this one in particular, are far more common in AI output than in human writing.
Fix: use a heading that fits the material ("Awards"), or fold the content into the body.

## 2. Language and grammar

### 9. High density of AI vocabulary
One or two of these can be coincidence; many together is one of the strongest tells. The list changes by model generation, and synonyms are not implicated, only these exact words.
- 2023 to mid-2024: additionally (especially opening a sentence), boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate/intricacies, interplay, key, landscape (abstract), meticulously, pivotal, underscore, tapestry (abstract), testament, valuable, vibrant.
- Mid-2024 to mid-2025: align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant.
- Mid-2025 to mid-2026: emphasizing, enhance, highlighting, showcasing, plus the notability phrasing in pattern 2.
- Mid-2026 on: challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally, with heavy use of periods and commas and short sentences.
- Grok specifically: causal, empirical, correlate, underscore.
- Also listed in the page's words to watch: deep dive, robust, showcase.
Fix: use the plain word. Often the sentence is better with no replacement at all.

### 10. Avoiding basic copulatives
"is" and "are" replaced by "serves as", "stands as", "marks", "represents"; "has" replaced by "features", "offers", "boasts", "maintains". Lead sentences that say "X refers to..." as if the article were about the word. Newer output stretches this: "ventured into politics as a candidate" for "was a candidate".
Fix: "is", "are", "has", "was".

### 11. Negative parallelisms
Constructions that correct a misconception nobody had.
- "Not only X but also Y", "It is not just X, it's Y", and the multi-sentence version ("X. Y, however, took a path that...").
- "Not X, but Y", "It's not X, it's Y", "no X, no Y, just Z".
- "Y rather than X", especially common in recent output.
Fix: state Y directly. Mention X only if a reader would really assume it.

### 12. Treating a list or broad title as a proper noun
Opening sentences that define the title of a list or general topic as if it were an entity ("List of songs about Mexico is a collection of...").
Fix: open with the subject itself.

### 13. Rule of three
"Adjective, adjective, adjective" or three short parallel phrases, used to make thin analysis look thorough. Stronger as a tell where nobody would bother with flourishes (edit summaries, commit messages).
Fix: give as many items as there are. Two is fine. One is fine.

### 14. Uniform, comma-and-period-only sentences (newer sign)
Since models were trained off em dashes, their output leans on commas and periods, with sentences clustered in an 8 to 20 word band.
Fix: vary length; use colons, semicolons and parentheses where natural.

## 3. Style

### 15. Title case in section headings
Fix: sentence case.

### 16. Overuse of boldface
Bold scattered through prose, or literal asterisks where bold was attempted.
Fix: bold almost nothing in running text.

### 17. Inline-header vertical lists
Bullets that each start with a bolded label and a colon.
Fix: prose, or a plain list.

### 18. Wrong heading levels
Starting with a level-1 title heading, or several level-1 headings.
Fix: follow the target format's conventions.

### 19. Emoji on headings or list items
Fix: none, unless the user wants them.

### 20. Curly quotes and apostrophes
Fix: straight " and '.

## 4. Text addressed to the user

### 21. Collaborative communication left in the text
Advice, offers and chat meant for the person prompting the model, pasted into the final text or hidden comments. Includes instructions to the user about what to check before publishing.
Watch: a Wikipedia-style article, I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., is there anything else, let me know, more detailed breakdown, here is a..., [check/verify/confirm] ... before [publishing/submitting].
Fix: deliver the text alone. No opener, no closer.

### 22. Hedging disclaimers about source availability and use
- 2023 to 2024: didactic "it's important to note" notes, safety advice to an imagined reader, jurisdiction caveats.
- 2024 to 2025: claims that information "is not publicly available" or "not widely documented", then speculation about what it "likely" is. For people: "maintains a low profile", "keeps personal details private".
- Mid-2026 on: corrective framings. "[Claim] should be treated as [speculative] rather than [definitive]"; "the available information does not establish [conclusion]"; "should not be confused with" (less reliable).
Watch: while specific details are limited/scarce, not widely available/documented/disclosed, in the provided/available sources, search results, based on available information, does not by itself establish.
Fix: if something is unknown, leave it out or say once that it is unknown. Don't speculate around the gap.

### 23. Phrasal templates and placeholder text
Fill-in-the-blank text the user forgot to fill: [Entertainer's Name], (Add your channel URL here), (If available), "Evidence to be supplied: [links]", infobox comments like "Add if available with citation". Date placeholders such as 2025-XX-XX in access dates. URL placeholders such as INSERT_SOURCE_URL or example.com/source1, example.com/article.
Fix: fill it with real information or remove it.

## 5. Markup and citations

### 24. Markdown where it doesn't belong
Asterisks for bold, # headings, --- dividers, [text](url) links in formats that use different markup, and whole outputs wrapped in ``` fences (often labeled "wikitext"). Leaked citation internals such as contentReference[oaicite:1] are unambiguous.
Fix: write in the target format's markup. Never leave tool artifacts.

### 25. Nonexistent categories or templates
Fix: only use ones you know exist.

### 26. Broken external links, invalid DOIs and ISBNs, DOIs pointing to unrelated papers
Several dead links that were never archived suggest the links were never real. ISBN checksums fail. DOIs resolve to unrelated work.
Fix: only cite sources you have actually opened.

### 27. Book citations without page numbers or URLs, or with pages that don't support the claim
Fix: give a page that you have checked says what you claim.

### 28. Incorrect or unconventional reference syntax
Broken attempts to reuse references, bare [3] markers, ↩ characters around footnotes.
Fix: use the format's real citation syntax.

### 29. Tracking parameters
utm_source=chatgpt.com, utm_source=openai, utm_source=copilot.com, referrer=grok.com.
Fix: strip them from every URL.

### 30. References defined but never used, or used but never defined
Fix: every reference you list is cited, and every citation resolves.

## 6. Comments and edit summaries

### 31. Customer-service tone in discussion
Claims of having "carefully reviewed", apologies for any inconvenience "you may have experienced", "If there are specific issues, please point them out". Openers like "Dear editorial team", "I am writing to...", "I hope this message finds you well", "I understand your concerns regarding...". Also: misquoted or invented policy shortcuts, sectioned long comments, playing down AI use, asking critics to do the work, calling concerns "unsubstantiated speculation".
Fix: short, direct, in your own voice.

### 32. Lengthy comments split into titled sections
Fix: a few plain sentences.

### 33. Template-style edit and change summaries
- Canned assurance of compliance: ensured that... adheres to, refined, enhanced, enriched, streamlined, improved, in compliance with, guidelines/style/standards, revised, verifiability, neutrality, neutral/encyclopedic tone, clarity, flow.
- Saying what was kept or avoided: preserved, retained, avoided, ensured, aimed to.
- Overemphasis on sourcing: added sourced content, added verified information, added citations/coverage, improved attribution, with independent/secondary/peer-reviewed sources.
- Itemizing parameter and template names with their markup.
- Announcing that edits address reviewer feedback.
- First-person summaries with emoji or Markdown (older); exhaustive procedural summaries (newer).
Fix: one line on what changed in the content. "Add 2019 album and tour dates", "Fix null check in parser".

## 7. Miscellaneous

### 34. Sudden shift in writing style
Polished text from someone whose other writing is very different, or a style that tracks each year's model output.
Fix: write in the user's own voice; match their existing text.

### 35. Submission statements
Notes to reviewers explaining why the draft meets guidelines and is notable.
Fix: let the content stand on its own.

### 36. Pre-placed maintenance templates
Drafts that arrive already tagged declined, or carrying maintenance or protection banners that make no sense for a new page.
Fix: don't add process markers the user didn't ask for.

### 37. Canned profile pages
"Welcome to my user page!", "About me", "My interests", "Let's connect!", with emoji and bold.
Fix: write it plainly, in the person's voice.

### 38. Many quick, low-value edits
Batches of throwaway rewrites across unrelated pages.
Fix: make only changes that improve something.

### 39. Pro-authoritarian bias
Models soften criticism of repressive governments and are harsher on freer ones, more so in some languages.
Fix: hold all governments to the same standard and follow the sources.

## 8. Older signs, mostly 2022 to 2025

### 40. Promotional, ad-like language
Watch: boasts a, vibrant, rich, profound, enhancing, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking, renowned, featuring, diverse array.
Fix: neutral description with facts.

### 41. Knowledge-cutoff statements
Watch: as of my last knowledge update, up to my last training update.
Fix: never include them.

### 42. Section summaries
Watch: In summary, In conclusion, Overall; "Conclusion" sections; paragraphs that end by restating themselves.
Fix: stop when the content is done.

### 43. Prompt refusals
Watch: as an AI language model, as a large language model, I cannot offer medical advice, but I can..., I'm sorry...
Fix: never include them in delivered text.

### 44. Em dashes
More of them than human writers use, often spaced, used where a comma, colon or parentheses would do, for punched-up emphasis. Newer models avoid them entirely, which created pattern 14.
Fix: none. Replace with whatever punctuation fits, and vary it.

### 45. Abrupt cut-offs
Text that stops mid-thought (older output limits).
Fix: finish, or shorten the scope.

### 46. Outdated access dates
Citations with access dates well before the edit.
Fix: use the date you actually checked the source.

### 47. Elegant variation
A repetition penalty pushes models to rename the same thing each time ("Soviet artistic constraints", "the challenging climate", "state-imposed artistic norms").
Fix: pick the right term and repeat it.

---

## 9. Signs of human writing (keep these)

The page lists constructions that are more common in human-written text than in AI text:

- simple is/has phrases ("there is a", "it has a")
- plain words over stiff synonyms: wrote/authored, moved/relocated, used/utilized, tried/attempted, died/passed away
- superlative or definite statements: "one of the best", "is the only", "was the first"
- qualifiers and intensifiers: "very", "perhaps", "tends to"
- ordinary wordy phrases: "as a result of", "in order to", "all of the", "a part of", "the fact that"

## 10. Signs that are not reliable

The page says these don't indicate AI on their own, so there's no need to avoid them: perfect grammar, mixing casual and formal registers, prose that sounds bland or robotic, fancy or academic vocabulary in general, a transition word used here and there, unsourced content, bizarre markup errors, and correct markup.
