# Hermes Agent: inspect memory before trusting recall

Checked **October 2, 2026**, against the current official documentation; verify commands with your installed version. This guide covers Hermes Agent by Nous Research, not unrelated products named Hermes.

1. Run `hermes memory status` to see active memory providers. Built-in memory and external providers are separate surfaces.
2. In chat, enter `/memory approval on`. Use `/memory pending`, read each proposed write, then `/memory approve <id>` or `/memory reject <id>`. This gates future built-in writes, not all external storage.
3. Run `hermes journey list`. Copy the exact node ID for a mistaken memory, then `hermes journey edit <node>` to edit it. `hermes journey delete <node>` removes that selected node after confirmation; deletion changes stored state.
4. For the default profile, inspect `~/.hermes/memories/MEMORY.md` and `USER.md`. A new session loads a fresh snapshot. Saved chats can still be retrieved through `session_search`; changing these two files does not delete conversation history.

[Persistent-memory controls and files](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/).

For separation, create a blank profile with `hermes profile create work`, then run `work setup` and `work chat`. Each profile has separate state. Avoid `--clone` for a fresh memory: it copies curated memory and configuration, and external-provider settings can still point at shared storage. Check that provider's isolation separately. [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles).

For a review, supply the relevant logs or documents and ask:

> Assess this conclusion from the attached evidence. Treat stored preferences as preferences. Identify any remembered claim affecting the assessment, its source, and whether that source supports it. Do not save new conclusions about people without showing the proposed entry.

This prompt requests disclosure; it cannot expose material the product does not make available. Check saved entries directly after a correction. Approval controls reduce accidental persistence; they do not establish that an approved claim is true.
