# Hermes Agent: manage memory and local chat history

Checked **October 3, 2026**, against Nous Research's official documentation and source revision `5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662`. Check the help for your installed version before using a command. These instructions describe Hermes Agent by Nous Research.

## Know which store you are changing

Hermes keeps curated notes in `MEMORY.md` and `USER.md` under the active profile's `memories/` directory. It also stores conversations, tool calls, and tool results in that profile's SQLite `state.db`. The `session_search` tool can retrieve previous conversations. Removing an entry from a memory file does not remove the chat that supplied it. [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/), [session storage](https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage/).

On macOS/Linux, the default profile's paths are `~/.hermes/memories/MEMORY.md`, `~/.hermes/memories/USER.md`, and `~/.hermes/state.db`. A named `work` profile uses `~/.hermes/profiles/work/` instead. Windows has a different platform default. Confirm the active profile and its home before reviewing files. Commands below use the active/default profile; put `hermes -p work` in place of `hermes` when reviewing `work`.

## Separate short notes from a shortened conversation

The configurable default budgets are 2,200 characters for `MEMORY.md` and 1,375 for `USER.md`. When a built-in memory write exceeds its budget, Hermes returns an error. The agent may then merge, replace, or remove entries to make room. That is different from shortening the conversation. There is no guarantee that a shorter note preserves every qualification in its source. [Bounded memory and source](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/), [checked store implementation](https://github.com/NousResearch/hermes-agent/blob/5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662/tools/memory_tool_store.py).

Hermes also compacts the live conversation when configured pressure thresholds are reached. `/compress` requests that operation manually. At the checked revision, default `compression.in_place: true` preserves the session ID and soft-archives earlier turns in `state.db`; they can remain searchable. Older rotating mode creates continuations. Compaction is not history deletion, and the shortened context can still contain a mistaken interpretation. [Dedicated compression guide](https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching).

Hermes can run a background review after a turn and save a durable memory or skill. A saved procedure is another possible source of repeated mistakes: inspect changed skills as well as notes. The product calls this background review, not dreaming. [Background review source](https://github.com/NousResearch/hermes-agent/blob/5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662/agent/background_review.py).

## Review saved notes and approve new ones

1. Run `hermes memory status` to identify configured memory providers. External providers have their own storage and controls.
2. Inspect the two memory files in an editor. `hermes journey list` also lists saved items; `hermes journey edit NODE_ID` opens a selected item's content. Replace `NODE_ID` with the exact ID from the listing.
3. In chat, enter `/memory approval on`. Read proposed writes using `/memory pending`, then `/memory approve ID` or `/memory reject ID`. This gate concerns built-in memory writes; it does not gate every possible external store or transcript write.
4. After editing memory, start a new session so the new system-prompt snapshot loads. Check the file instead of relying on the assistant's claim that it saved or removed something. [Built-in memory controls](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/).

For a saved interpretation such as “Jordan is blocking the project,” check the original exchange before rewriting it. A useful correction might be: “Alice suspected Jordan was blocking the project on October 2; his motive was not established.” Inspect later notes, skills, and provider records that repeat the same interpretation. Test the revised conclusion in a new session using the evidence, without telling the model which result you want.

## Pause automatic review separately

To pause automatic post-turn review in the intended profile:

```sh
hermes config set auxiliary.background_review.enabled false
```

That does not disable foreground writes, local transcripts, manual `/refine`, or external-provider synchronization. Finish or stop an already running review before assuming it is quiet. Restore its recorded previous value when appropriate. The separate `display.memory_notifications` setting can make writes more visible; switching notifications off only hides them. [Review controls](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/), [review implementation](https://github.com/NousResearch/hermes-agent/blob/5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662/agent/background_review.py).

## Pause recall without pretending that recording has stopped

Close the existing chat, then disable both built-in stores in the intended profile:

```sh
hermes config set memory.memory_enabled false
hermes config set memory.user_profile_enabled false
```

To stop the normal past-chat search tool as well, add `session_search` to the existing `agent.disabled_toolsets` list in that profile's `config.yaml`. This is a separate setting. Check the existing value first:

```sh
hermes config get agent.disabled_toolsets --json
```

If that list is empty, set it with:

```sh
hermes config set agent.disabled_toolsets '["session_search"]'
```

If other toolsets are already disabled, keep them in the list. For example, an existing `web` restriction becomes `["web", "session_search"]`. `config set` replaces the list; it does not append to it. Restart the chat or gateway to apply the configuration to a new session. [Global toolset controls](https://hermes-agent.nousresearch.com/docs/user-guide/configuration/#global-toolset-disable), [tool definitions at the checked revision](https://github.com/NousResearch/hermes-agent/blob/5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662/toolsets.py).

These changes leave the files and saved chats in place, and ordinary sessions still record new history. They do not create an incognito session. An external provider configured through `memory.provider` also needs its own review: turning off the two built-in stores does not disable it. `hermes memory off` separately clears the external-provider selection for newly initialized agents; it does not delete that service's records. Restart the affected runtime and begin a new session. Disabling a search tool also does not make readable local files inaccessible to other tools. Use a separate profile or stronger account/container boundaries when isolation is the goal. [Initialization](https://github.com/NousResearch/hermes-agent/blob/5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662/agent/agent_init.py), [transcript persistence](https://github.com/NousResearch/hermes-agent/blob/5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662/agent/session_persistence.py).

To restore built-in memory, restore both flags to their recorded previous values and remove only your added `session_search` restriction. Preserve any restrictions that were there before.

## Remove a chat or review a cleanup batch

`/new` starts a new thread. `/compress` reduces the current context. Archiving hides a chat from listings. None of these deletes stored history.

1. Close the chat you intend to remove. Wait for active turns and compression to finish. Stop other Hermes processes using that profile before bulk cleanup; a running chat can save its in-memory transcript again.
2. List sessions and copy the relevant ID:

```sh
hermes sessions list --limit 50
```

3. If you want an archive, export that session first. Replace `SESSION_ID` with its ID:

```sh
hermes sessions export session.jsonl --session-id SESSION_ID
```

4. To delete that stored session and its messages, run the following and review the confirmation:

```sh
hermes sessions delete SESSION_ID
```

5. For older sessions, preview the batch before changing anything:

```sh
hermes sessions prune --older-than 30 --dry-run
```

If the preview matches what you want removed, use the same selection without `--dry-run` and review the confirmation:

```sh
hermes sessions prune --older-than 30
```

Pruning selects ended sessions and normally excludes pinned and archived sessions. It uses last activity, not just the date a long conversation began. Additional filters can change the default age selection, so keep an explicit age limit. [Sessions and cleanup](https://hermes-agent.nousresearch.com/docs/user-guide/sessions/), [command parser](https://github.com/NousResearch/hermes-agent/blob/5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662/hermes_cli/subcommands/sessions.py).

After cleanup, check any related memory entries, continuation or branch sessions, external memory providers, and copies you exported or backed up. A single-session deletion does not remove every separate continuation, copied document, backup, or record held by the model provider. [Deletion implementation](https://github.com/NousResearch/hermes-agent/blob/5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662/hermes_state_sessions.py).

If your intention is specifically to clear both built-in note files, `hermes memory reset --target all` has a confirmation step. It does not clear `state.db`, provider records, or saved skills. This is a deliberate reset, not a weekly housekeeping command. Preserve any sources needed to explain actions the agent already took. [Memory command parser](https://github.com/NousResearch/hermes-agent/blob/5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662/hermes_cli/subcommands/memory.py).

## Inspect an external memory provider

At the checked revision, Hermes selects one external provider at a time. It supplements the built-in stores. Inspect its extraction and retrieval separately: an approval for a built-in note is not an approval for every provider write. [Provider architecture](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers/).

Mem0 is a concrete example. Automatic turn synchronization sends selected user and assistant text for extraction; the configurable default cap is 450 characters per message. An explicit `mem0_add` saves supplied text without that extraction. Use returned IDs with `mem0_search`, `mem0_update`, and `mem0_delete` when reviewing a particular record. Ordinary recall filters by `user_id`, across agents and channels, so changing `agent_id` alone does not isolate a work profile. Review the actual user namespace, storage, and access controls, then test with harmless facts. [Pinned Mem0 plugin](https://github.com/NousResearch/hermes-agent/blob/5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662/plugins/memory/mem0/__init__.py), [vendor integration](https://docs.mem0.ai/integrations/hermes).

Honcho and Hindsight use different representations and controls. The [memory-services guide](memory-services.md) compares them with Mem0 and Letta, including source attribution and correction. A locally stored database can still use remote extraction or embedding models; inspect those endpoints before calling the whole pipeline local.

## Separate work from personal use

Create a blank profile rather than copying the old profile's memories:

```sh
hermes profile create work
work setup
work chat
```

The new profile has its own memory files, configuration, and session database. Avoid `--clone` for this purpose: it copies curated memory and provider configuration. An external provider can still point both profiles at shared storage. [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles/).

Profiles separate normal state, but they are not an operating-system access boundary. At the checked revision, `session_search` can explicitly read another profile when supplied its name, and file tools can access files allowed by their environment. Use separate OS accounts, constrained containers, or separate hardware when one assistant must be unable to read the other's data. [Past-chat search implementation](https://github.com/NousResearch/hermes-agent/blob/5d3c05977bb3c8b7cfd6b3e39d96f6e35a9e0662/tools/session_search_tool.py).

## A review prompt

> Assess this conclusion from the attached evidence. Treat stored preferences as preferences. Identify any remembered claim affecting the assessment, its source, and whether that source supports it. Propose corrections separately. Show me each proposed memory change before saving it, and do not delete chats or modify provider configuration without my approval.

The prompt can help organize a review. Verify the resulting file, setting, or deletion yourself; a fluent confirmation is not evidence that an operation happened.
