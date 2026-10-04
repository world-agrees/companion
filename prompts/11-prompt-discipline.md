# Prompt discipline: a small catalogue

Use these with the evidence needed for the task and the appropriate project or fresh-chat controls already selected. A request to ignore prior preferences cannot technically disable memory, retrieved history, connectors, or provider instructions. The prompts make claims easier to check; they do not guarantee an objective or complete answer.

## 1. Turn a conclusion into a question

```text
My initial view: [what I currently believe]
Decision question: [what needs assessing]
Sources: [documents, dates, and precise locations]
Criteria: [requirements and legitimate priorities]

Restate my disputed conclusion as a neutral question that can be
investigated. Preserve the actual facts and criteria. Then assess
that question using the sources. Treat my view as a hypothesis,
not evidence. Do not infer the answer I would prefer and use that
inference to determine factual claims. Identify missing evidence.
```

Question reframing has experimental support in *Ask don't tell: Reducing sycophancy in large language models*. The exact prompt above is an adaptation for this book, not the researchers' tested prompt. Their study is a mitigation result, not a guarantee for every model or task.

## 2. Require evidence before the recommendation

```text
Assess [decision] against [criteria] using [named sources].
First list the facts that matter, with the page, clause, row, or
message date supporting each. Separate what the source says,
what I reported, what you infer, and what is still unknown.
For a disputed document claim, include the relevant short quote.
State when a source is inaccessible; do not invent its contents.
Then make a provisional recommendation. Name the evidence that
would change it. Keep unsupported claims out of the conclusion.
```

Open consequential citations yourself. A genuine document can be cited for a claim it does not support.

## 3. Verify the arithmetic

```text
For every calculation that determines this decision, identify
the input values and their source rows, units, formula, and
result. Use an available calculator or executable check when
appropriate and say which checks you actually performed.
Keep estimates labeled as estimates. Do not fill a missing
value with a guess. Report the effect of unresolved inputs.
```

For the scheduling example, eight plus seven plus five hours is twenty hours. Fourteen available hours leave a six-hour shortage. Changing the tone of the recommendation cannot supply those hours.

## 4. Ask for balance without ordering a performance

```text
Apply the same criteria to [options]. Identify genuine support,
the strongest relevant objection, and unresolved evidence for
each. Give unequal evidence the weight it deserves. Do not
invent criticism, praise, or a matching objection simply to make
the answer sound balanced. If the evidence favors one option,
say why. If it cannot decide, say what is missing.
```

“Find ten reasons I am wrong” can recruit an assistant to produce a different desired answer. Specific criteria and sources provide a better basis for review.

## 5. Detect a verdict that changed without new evidence

```text
Compare your earlier recommendation with the current one.
For each material change, identify the new evidence and source
that justified it. Distinguish new facts, changed priorities,
and my dissatisfaction with the earlier answer.
If no relevant evidence or criterion changed, reassess using
the original sources and criteria. Preserve supported warnings.
```

Use the existing [preference-pressure prompt](10-test-preference-pressure.md) for a controlled comparison in separate contexts. The legitimate priority “I need a cheaper option” can change a recommendation; “I really want this to be affordable” cannot change its quoted price.

## 6. Evaluate newly available evidence

```text
Reassess [decision] using these additional sources: [identifiers,
dates, versions, and permitted messages or documents].
Identify what is new, what contradicts the earlier assessment,
and what remains unchanged. Do not preserve an earlier conclusion
merely because it appears in our history. Cite the evidence for
any revised finding and identify older advice needing review.
```

Provide a relevant, authorized selection from the team's discussion, not only the messages supporting your account. Record the period and channels reviewed and any access gaps. The assistant cannot inspect colleagues' unrecorded conversations or assume that the available messages capture every part of a relationship.

## Sources checked October 3, 2026

- [Dubois and colleagues, Ask don't tell, version 4, July 29, 2026](https://arxiv.org/abs/2602.23971v4): controlled evidence for question reframing.
- [Anthropic, Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations): uncertainty, source quotations, and citation checking; remaining limitations.
- [James Phoenix and Mike Taylor, Prompt Engineering for Generative AI, O'Reilly, May 2024](https://www.oreilly.com/library/view/prompt-engineering-for/9781098153427/): its five principles cover direction, format, examples, evaluation, and division of work. The publisher's contents also identify reference grounding and criteria evaluation in Chapter 3. The book is broader prompting guidance, not evidence that a prompt can eliminate sycophancy.
