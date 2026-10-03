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
