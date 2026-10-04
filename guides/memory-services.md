# Agent memory services: inspect the extra store

Checked **October 3, 2026** against the primary documentation linked below. This guide assumes the agent and any selected service are already installed. It does not configure accounts, install plugins, or contact a service. Match the instructions to your installed versions.

An additional memory service can retrieve project history that no longer fits in a conversation. It can also preserve a mistaken conclusion and supply it to a new task. A long-running agent may then use that conclusion while writing files, scheduling work, or preparing a decision. Review what enters that store, what comes back, and what happens when you correct it.

## What these services do

| System | Memory approach | Documented connection to these agents | What to inspect |
| --- | --- | --- | --- |
| **Mem0** | Extracted memories with identifiers, metadata, and semantic retrieval; explicit update/delete operations. Managed Platform and self-managed OSS are different deployments. | Hermes provider and the vendor's `@mem0/openclaw-mem0` plugin. | Exact memory IDs, user scope, original messages, automatic capture/recall settings, and whether updates reach all copies. |
| **Honcho** | Models users and agents as peers. It derives conclusions and representations from their messages. | Official Hermes integration and `@honcho-ai/openclaw-honcho`. | Source messages, peer/workspace identities, conclusions, and which conclusions were inferred from other conclusions. |
| **Hindsight** | Retains source documents and extracted facts, retrieves memories, and synthesizes answers. Background consolidation creates observations with source links. | Maintainer-documented Hermes and OpenClaw plugins. | Bank, document ID, facts, observations, retention roles, and derived observations after a source changes. |
| **Letta** | A stateful agent platform. Its current MemFS memory uses git repositories, with some files always in context and other files read on demand. | An alternative platform for building agents; this review did not establish a drop-in Hermes or OpenClaw provider. | Committed memory changes, files at the memory root (or `system/` in older agents), shared repositories, and dreaming settings. |

Sources: [Mem0 operations](https://docs.mem0.ai/core-concepts/memory-operations/add), [Hermes integration](https://docs.mem0.ai/integrations/hermes), [OpenClaw integration](https://docs.mem0.ai/integrations/openclaw); [Honcho Hermes](https://honcho.dev/docs/v3/guides/integrations/hermes), [Honcho OpenClaw](https://honcho.dev/docs/v3/guides/integrations/openclaw); [Hindsight retain](https://hindsight.vectorize.io/developer/retain), [observations](https://hindsight.vectorize.io/developer/observations), [Hermes](https://hindsight.vectorize.io/sdks/integrations/hermes), [OpenClaw](https://hindsight.vectorize.io/sdks/integrations/openclaw); [Letta memory](https://docs.letta.com/agent-sdk/memory).

## Mem0: correct the record you actually retrieve

Mem0's current `add` documentation describes extraction when `infer=True` and raw storage when `infer=False`. It describes additions as accumulating memories; do not assume a new contradictory message retires an older one. Locate the old ID, inspect its content and source, and use the documented [update](https://docs.mem0.ai/core-concepts/memory-operations/update) or [delete](https://docs.mem0.ai/core-concepts/memory-operations/delete) operation when appropriate. Search again afterward. A search result's relevance score does not verify its truth.

For an existing OpenClaw Mem0 plugin, begin with read-only inspection:

```sh
openclaw mem0 help --json
openclaw mem0 status --json
openclaw mem0 list --json
openclaw mem0 search "project readiness" --scope long-term --json
```

The integration documents separate `autoCapture` and `autoRecall` controls under `plugins.entries.openclaw-mem0.config`. Turning either off stops that automatic hook; it does not remove stored memories or prevent explicit memory-tool calls. [Plugin controls](https://docs.mem0.ai/integrations/openclaw).

For Hermes, check `hermes memory status`, then review the active profile's `mem0.json`. The checked Hermes implementation searches by `user_id`, across agents and channels. Changing only `agent_id` is not a reliable way to isolate work from home. See the [Hermes guide](hermes.md) for the pinned source and controls. A local vector database can still send text to remote extraction and embedding models; “self-hosted storage” does not establish that all processing is local.

## Honcho: inspect what was inferred about you

Ask the agent to retrieve your profile and the relevant source messages before asking Honcho for a synthesized answer. Its current MCP documentation exposes conclusion attribution: `level` distinguishes direct extraction from deductive, inductive, and contradiction-derived conclusions; `source_ids` links derived conclusions to their inputs. Follow those links when correcting a conclusion. [Honcho source and attribution](https://github.com/plastic-labs/honcho/blob/main/mcp/instructions.md).

Hermes's Honcho configuration includes `saveMessages`, `recallMode`, and workspace/peer identities. Pausing new message storage is different from disabling retrieval. An OpenClaw migration can upload old files while leaving originals intact. A correction in the service therefore does not revise those original files. Inspect both. [Hermes controls](https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho/), [OpenClaw migration](https://honcho.dev/docs/v3/guides/integrations/openclaw).

## Hindsight: follow facts into observations

Inspect the relevant bank and document before judging the resulting observation. Hindsight documents source-backed observations, background consolidation, and invalidation of observations when their source memories are deleted. Document updates and deletions have different effects; a [document deletion](https://hindsight.vectorize.io/developer/api/documents) permanently removes the associated memories. Verify the affected observations and any remaining source documents after a correction. [Observation lifecycle](https://hindsight.vectorize.io/developer/observations).

The integrations expose separate automatic retain and recall controls. They also expose extraction and consolidation missions: instructions about what information to preserve. Inspect those instructions rather than assuming they are neutral. In Hermes, the documented `bank_id_template` can create a separate bank per profile. An identifier is still not an access-control guarantee. [Hermes configuration](https://hindsight.vectorize.io/sdks/integrations/hermes), [OpenClaw configuration](https://hindsight.vectorize.io/sdks/integrations/openclaw).

## Letta: review the memory repository

Use Letta's current memory viewer or the agent's MemFS directory to inspect stored information. Review git changes as well as the current text. In the current layout, files at the memory root enter the system prompt each turn; older agents use `system/`. Indexed subdirectories can remain outside context until read. Shared repositories make an edit available to more than one agent. [MemFS](https://docs.letta.com/concepts/memfs), [shared repositories](https://docs.letta.com/agent-sdk/repositories).

Current CLI/app documentation offers `/doctor` for a memory audit and `/sleeptime` or app Dream settings for background consolidation. “Agent reviews before applying” means another model conversation reviews the change; it does not request your approval. Older V1 SDK memory-block examples belong to a different API generation. [Current memory and dreaming](https://docs.letta.com/configuration/memory), [legacy blocks](https://docs.letta.com/v1-sdk/memory/memory-blocks).

## A weekly review for a long-running agent

1. Identify every store and writer: files, transcripts, indexes, providers, background jobs, and any shared banks or repositories.
2. Review newly saved claims and a few memories retrieved during consequential tasks. Check speaker, date, uncertainty, and original source.
3. Retire incorrect or expired claims. Find summaries and recommendations derived from them; recompute those or hold them for review.
4. Use a new session and a neutral question to test the correction. Restart the agent as well when testing persistence. Check retrieved records, not only its reassuring reply.
5. Check separation using harmless synthetic facts in each intended scope. Investigate any cross-scope retrieval before using sensitive material.
6. Save a dated review record stating what changed and what could not be inspected. If a job continues using a disputed premise, pause that job until its inputs are corrected.

These are proposed maintenance practices. They make errors easier to find and correct; this guide does not present a measured anti-sycophancy treatment or a guarantee of complete deletion.

Try the two [offline Python demonstrations](../developer/README.md) before experimenting with a real store. They show why preserving qualifications and propagating corrections matter without accessing your agent's memory.
