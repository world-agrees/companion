# OpenClaw: inspect files, compaction, and consolidation

Checked **October 3, 2026**, against the official documentation and source revision `9e32882cdf46a91b082ce1cf2326d872c8bbac25`. This guide assumes OpenClaw is installed. Compare `openclaw memory --help` and `openclaw config --help` with your installed release before making changes. Commands use the agent `main`; replace it with the intended agent ID.

## Locate the actual stores

Begin with:

```sh
openclaw config get agents.entries.main
openclaw memory status --agent main --json
openclaw sessions --agent main --limit all --json
```

The default workspace is `~/.openclaw/workspace`, but your agent can use another directory. With the normal file-based setup, inspect `USER.md` for preferences, `MEMORY.md` for durable notes, and `memory/YYYY-MM-DD.md` or dated variants for working notes. `DREAMS.md` is a consolidation diary, not the source from which durable facts are promoted. [Memory overview](https://docs.openclaw.ai/concepts/memory).

Core search indexes these sources. The per-agent SQLite database can also hold sessions and other durable state: do not delete that database or its sidecars to clear a memory index. Use memory-specific recovery commands. Missing search results do not establish that a fact was never saved. [Built-in storage](https://docs.openclaw.ai/concepts/memory-builtin).

Search for a particular premise and inspect its source:

```sh
openclaw memory search --agent main --query "release approval" --json
```

Search may contact the configured embedding provider. Plain status is lighter than `--deep`, which can probe a provider. Status `--index` and `--fix` perform work; they are not merely inspection. [CLI behavior](https://docs.openclaw.ai/cli/memory).

## A new chat, compaction, and dreaming are different

Bare `/new` or `/reset` can load today's and yesterday's daily notes. A fresh conversation is not necessarily blank memory. `/context list` and `/context detail` help inspect what the agent sees, including files whose injected copies are shorter than the files on disk. [Startup and context](https://docs.openclaw.ai/concepts/memory).

Compaction shortens the live conversation while leaving its full history on disk. Built-in `/compact` requests it manually. Before automatic compaction, a memory flush can give the agent a silent opportunity to save durable context. That saved note may preserve a useful finding or a mistaken interpretation. Compaction, saving, and erasure are distinct operations. Native runtimes can behave differently. [Compaction](https://docs.openclaw.ai/concepts/compaction).

Memory-core's default-on dreaming stages candidates, reflects on them, and promotes selected durable entries. Inspect the source references and changes to `MEMORY.md`, not only the diary. The following commands preview promotion; `rem-harness` can call a model even though it does not write:

```sh
openclaw memory promote --agent main --json
openclaw memory promote-explain "release approval" --agent main --json
openclaw memory rem-harness --agent main --json
```

Adding `--apply` to promotion makes changes. In chat, `/dreaming status` inspects; `/dreaming off` pauses automatic dreaming when issued by an authorized owner/admin. [Dreaming controls](https://docs.openclaw.ai/concepts/dreaming).

## Pause the operation you intend to pause

| Goal | Documented control | What this does not do |
| --- | --- | --- |
| Pause memory-core dreaming | `/dreaming off` | Erase notes, pause retrieval, or stop unrelated jobs. |
| Stop search for `main` | `agents.entries.main.memory.search.enabled: false` | Remove bootstrap files or saved history. |
| Stop automatic pre-compaction saving | `agents.defaults.compaction.memoryFlush.enabled: false` | Stop compaction or other writes. |
| Disable the memory plugin slot | `plugins.slots.memory: "none"` | Erase state or disable every independent integration. |

Changing `memory.search.provider` to `"none"` means keyword-only search; it does **not** disable search. [Memory settings](https://docs.openclaw.ai/reference/memory-config), [search behavior](https://docs.openclaw.ai/concepts/memory-search).

Save existing values first. For a chosen change, use the configuration CLI's preview, inspect it, then apply that same setting:

```sh
openclaw config set agents.entries.main.memory.search.enabled false --strict-json --dry-run
openclaw config set agents.entries.main.memory.search.enabled false --strict-json
openclaw config validate
```

These are examples, not an automatic maintenance batch. Follow the reload/restart hint and verify runtime status. Restore saved values when resuming; do not assume all prior values were `true`. Independently pause scheduled work and other writers when correcting a premise that could drive actions. [Configuration CLI](https://docs.openclaw.ai/cli/config).

## Correct sources, then rebuild and test

Suppose a recurring task retrieves “Friday release approved,” while the original approval depended on two tests passing. Merely clearing the search index leaves the incorrect note available to be indexed again.

1. Identify the intended agent, workspace, memory plugin, and any external stores. Pause affected work and writers before editing.
2. Check the original approval and test log. Correct or explicitly supersede the false claim in its actual source file. Preserve the date, source, and condition.
3. Find later summaries and provider entries that repeat it. Recompute them or hold them for review. A changed note does not undo a recommendation already delivered.
4. Rebuild the intended core index and search again:

```sh
openclaw memory index --agent main --force
openclaw memory search --agent main --query "release approval" --json
openclaw memory status --agent main --json
```

5. Begin a controlled new task and check which records it retrieves. An old compacted conversation can still contain the earlier conclusion. Resume the recurring task only after verifying its corrected inputs.

`openclaw memory reset --agent main` clears the derived core index/cache after confirmation. It preserves sources that can be indexed again. Omitting `--agent` broadens the reset to all configured agents. [Correction and recovery](https://docs.openclaw.ai/cli/memory), [provenance](https://docs.openclaw.ai/concepts/memory-provenance).

## Remove tracked session-derived material

If you intend to remove material derived from a particular session, get its exact ID/key from the intended agent's session list, then preview:

```sh
openclaw memory forget --agent main --session SESSION_ID --dry-run --json
```

Inspect the resolved sessions, entries, mixed lineage, artifacts, and curated-file changes. Only if this is the intended cleanup, repeat without `--dry-run`. **It applies immediately without another confirmation.** Mixed-origin entries can be removed whole. Resolve partial errors before retrying. [Forget semantics](https://docs.openclaw.ai/concepts/memory-provenance).

This core command removes identifiable tracked material and excludes selected sessions from later ingestion. Original transcripts, handwritten edits, other agents' stores, exports, backups, and another plugin's database may remain. It is not a complete privacy purge. Preserve records needed to explain actions already taken.

## Check the active plugin and companion layers

The core commands above do not universally manage other stores. Memory-core can remain a consolidation sidecar when another plugin owns the active slot; a core reset/forget can affect that sidecar without correcting the plugin's database.

The official external `@openclaw/memory-lancedb` plugin has its own automatic capture/recall controls and `openclaw ltm` inspection commands. Its `memory_forget` tool removes its records; that is different from core's session-based CLI forget. [LanceDB plugin](https://docs.openclaw.ai/plugins/memory-lancedb).

The vendor-maintained Mem0, Honcho, and Hindsight integrations each introduce their own storage and background processing. Honcho can run alongside local file search. The bundled Memory Wiki is another companion layer with source claims and compiled context; it does not replace the memory slot. Its default global scope also needs review when agent separation matters. [Honcho](https://docs.openclaw.ai/concepts/memory-honcho), [Memory Wiki](https://docs.openclaw.ai/plugins/memory-wiki), [memory-services comparison](memory-services.md).

For a consequential task, request:

> List the source files and memory entries used for this assessment. Quote the relevant evidence with dates or versions. Separate observations from inferences. If a remembered conclusion conflicts with the original, use the original and flag the memory for review. Identify stores or hidden context you cannot inspect. Propose changes before applying them.

The agent can only report what it can inspect. Verify actual files, retrieved records, and runtime settings. These practices make mistakes easier to review; they are not demonstrated guarantees against sycophancy. The [offline Python examples](../developer/README.md) let you examine compaction and persistent correction using synthetic data.
