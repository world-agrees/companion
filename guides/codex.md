# Codex: make project instructions and memory inspectable

Checked **October 2, 2026**, using official OpenAI documentation. These are local Codex controls, separate from ChatGPT web memory. Interfaces and managed settings may differ.

1. In an interactive Codex CLI session, enter `/memories`. Choose separately whether this chat may use existing local memories and contribute to future memories. If unavailable, check your version and documented configuration.
2. In the desktop app, use **Settings → Personalization** for local memories. The official guide currently describes the feature as off by default. Generated files live under the Codex home, usually `~/.codex/memories/`; inspect them for troubleshooting, but use supported controls rather than hand-editing generated state. [Local memory guide](https://learn.chatgpt.com/docs/customization/memories).

For configuration-based control, merge this into the existing `config.toml`, preserving other settings:

```toml
[memories]
use_memories = false
generate_memories = false
```

The first disables injection into future sessions; the second excludes newly created chats as memory-generation inputs. This does not delete existing files or remove project instructions. Restart the client when changing configuration and check its reported settings. [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

3. Put required project guidance in its root `AGENTS.md`. Review applicable global instructions and nested overrides too. Start a new session from the intended directory and ask it to list active instruction sources. Treat that response as a check to compare with the files, not a complete audit of every internal instruction. [Instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
4. For an optional reusable workflow, copy one resource-kit skill folder into your repository's `.agents/skills/`. Invoke it by its skill name where the client supports selection. Repository skills contain a `SKILL.md` with `name` and `description`; local discovery differs from publishing a plugin. [Build skills](https://learn.chatgpt.com/docs/build-skills).

Suggested project rule:

> Judge a change from code, requirements, and reproducible results. Report relevant files and lines, commands actually run, and failures. Do not infer correctness from my confidence or insistence. Preserve important limitations when summarizing. Mark a model inference as an inference.

A smaller remembered context helps inspection; it does not replace review or testing.
