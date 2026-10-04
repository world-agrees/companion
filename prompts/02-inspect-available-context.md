# Inspect available context

This prompt asks what the assistant can actually observe. Its answer is not an exhaustive provider disclosure. Inspect product settings, project files, source viewers, connectors, and tool logs separately. If a developer-controlled application supplies an input manifest, compare it with the answer.

## Copy and adapt

```text
Before assessing [task], inventory the inputs you can directly
observe for this request. Separate:
1. material I supplied in this conversation;
2. project or workspace files and instructions you can inspect;
3. retrieved material, with source identifiers and versions;
4. saved memory or prior summaries actually made available to you;
5. tools you used and the material they returned.

For each item, say whether you inspected it or it was only named.
Distinguish source text from a prior assistant inference.
Identify conflicting dates, superseded records, and missing inputs.

Do not invent a memory, source, or instruction to complete the list.
If a category is not visible to you, label it unknown. Do not claim
this inventory reveals every hidden instruction or provider input.

Identify which observed inputs are relevant to this task and why.
Do not start the substantive assessment yet.
```

## Check the result

Compare it with your source and context manifests. Correct a missing attachment, wrong version, or unrelated retrieved memory before proceeding. A product may not expose every retrieval or internal instruction; retain that uncertainty in your own record.

## Try it with a restaurant question

The author used this exact prompt in ChatGPT, with GPT 6.1 Sol and High reasoning, on October 3, 2026. Chapter 8 discusses an excerpt; Appendix A reproduces the complete response. The response separated stated preferences, reported information, interpretations, and claims attributed to connected records.

```text
When I ask you a question about where I should eat tonight you use some of my history.  Can you list the personal context you can identify for this request. Separate my preferences, things I reported, your interpretations, and claims supported by a document. For each claim, name its source and date if available. Flag uncertainty. Say which context you cannot inspect. Do not fill the gaps with guesses.
```

Use the result to find sources you can inspect. Treat the assistant's source descriptions and confidence ratings as claims to check. The inventory need not reveal everything the service can access.
