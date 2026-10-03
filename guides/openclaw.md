# OpenClaw: inspect retrieval and consolidation

Checked **October 2, 2026**. These commands describe the documented `memory-core` plugin. Other memory plugins can behave differently; compare `openclaw memory --help` with the documentation for your installed release.

1. Run `openclaw memory status --agent main` and `openclaw memory search --agent main --query "release" --json`, replacing the agent and topic. Investigate a `stale` warning before treating missing matches as proof nothing was saved.
2. To remove material derived from a specific session, preview `openclaw memory forget --agent main --session SESSION_ID --dry-run --json`. Inspect the report. Only if you intend that deletion, repeat without `--dry-run`; it deletes immediately. Source transcripts remain.
3. If you intend to clear that agent's derived index, use `openclaw memory reset --agent main`. Retained sources can be indexed again. Omitting `--agent` resets all configured agents. [CLI commands](https://docs.openclaw.ai/cli/memory).

Before background consolidation, enter `/dreaming status`. If you want to stop automatic dreaming, use `/dreaming off` as an authorized owner. Inspect the Dream Diary in `DREAMS.md` and the actual durable entries in `MEMORY.md`; the diary is not itself a promotion source. Preview consolidation with `openclaw memory rem-harness --agent main --json` or `openclaw memory promote --agent main`; `--apply` makes promotion changes. [Dreaming](https://docs.openclaw.ai/concepts/dreaming).

Choose the workspace belonging to the intended agent before reviewing its files. Other memory backends may store additional material. [Memory overview](https://docs.openclaw.ai/concepts/memory).

Compare entries against originals: who said it, was it checked, what qualification disappeared, and what later advice used it? Preserve a useful correction rather than merely clearing an index that will reread the same incorrect source.

For a consequential task, request:

> List the source files and memory entries used for this assessment. Quote the relevant evidence with dates or versions. Separate observations from inferences. If a remembered conclusion conflicts with the original, use the original and flag the memory for review.

The agent can only report what it can inspect. These controls make consolidation reviewable; they are not demonstrated guarantees against sycophancy.
