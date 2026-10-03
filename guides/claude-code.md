# Claude Code: inspect instructions and generated memory

Checked **October 2, 2026**, against current official documentation. This guide covers local Claude Code, whose project files and auto-memory are separate from consumer Claude's memory controls. Commands may differ in older clients; no live configuration was changed or tested for this guide.

1. Enter `/context` and inspect **Memory files**. Review the listed instructions, including applicable `~/.claude/CLAUDE.md`, project `CLAUDE.md` or `.claude/CLAUDE.md`, and `CLAUDE.local.md`. Ancestor instructions load at launch; nested instructions load when relevant files are read. These files are combined, so a narrower file does not reliably cancel a conflicting instruction.
2. Enter `/memory` and open an **existing** listed file or auto-memory directory. Inspect `MEMORY.md` and relevant topic files. Correct or delete a mistaken note in your editor. Also find summaries that repeated it; retain the source and correction date. Repository worktrees normally share auto-memory, so a new worktree alone does not isolate it.
3. To stop auto-memory, use the `/memory` toggle; it saves a user setting. For one project, merge `"autoMemoryEnabled": false` into `.claude/settings.json`. For one Bash/Zsh launch, use `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude`. These disable auto-memory, not existing instruction files or manual file access. Saved notes remain. Restart and inspect `/context` and `/memory` again. [Memory and instruction controls](https://code.claude.com/docs/en/memory).

4. Enter `/permissions` to inspect rules and their originating settings files. If a project contains a `personal/` directory that this coding task must not use or change, merge this example into that project's `.claude/settings.json`, preserving existing rules:

```json
{
  "permissions": {
    "deny": [
      "Read(/personal/**)",
      "Edit(/personal/**)"
    ]
  }
}
```

Here `/personal/**` is relative to the project working directory. These rules cover built-in file tools; arbitrary subprocesses and remote MCP services need their own controls. Review Bash/MCP permissions and sandbox restrictions too. An instruction to avoid a folder is not an access barrier. Reopen `/permissions` to confirm the rules and their scope. [Permissions and path syntax](https://code.claude.com/docs/en/permissions).

5. Use `/clear` to start a new conversation for an unrelated task. The previous conversation remains resumable; this is not deletion. [Interactive session behavior](https://code.claude.com/docs/en/interactive-mode). Stored instructions and enabled auto-memory can still supply context. To shorten an ongoing conversation, `/compact <instructions>` requests a summary rather than preserving every detail. For example:

```text
/compact Preserve failed tests, unresolved assumptions,
source paths, and the next checks.
```

Type that as one command. Keep original evidence outside the summary and reopen it before a consequential decision. [Compaction guidance](https://code.claude.com/docs/en/best-practices).

Suggested review prompt:

> Evaluate this change against the requirements and files I specify. Give file paths and lines, commands actually run, and observed results. Separate failures, assumptions, and untested claims. Check whether stored notes conflict with the current code. My preferred conclusion is not evidence. Do not record a conclusion as verified unless the supporting check exists.

This proposed workflow makes review easier; it does not prove that a response is free of sycophancy.
