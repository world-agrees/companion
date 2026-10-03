# GitHub Copilot: memory, instructions, and checkpoints

Checked **October 2, 2026**. This is GitHub Copilot for coding; Microsoft Copilot and Microsoft 365 Copilot have different controls. Copilot Memory is documented as a public preview on paid plans, with organizational policies affecting availability. Repository facts and personal preferences are distinct; personal preferences can follow a user across repositories. [Memory overview](https://docs.github.com/en/copilot/concepts/agents/copilot-memory).

1. On GitHub, click your profile picture → **Copilot settings** → under **Features**, find **Copilot Memory** and choose **Enabled** or **Disabled**.
2. For your preferences, use profile picture → **Copilot settings** → **Memory** in the sidebar. Review and delete incorrect entries.
3. As repository owner, use repository → **Settings** → **Copilot** → **Memory** to review or delete repository facts. Turning off future memory use is different from correcting already stored entries. [Management steps](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/copilot-memory/manage-for-yourself).

In **Copilot CLI**, enter `/context` to see context usage. After compaction, run `/session checkpoints`, then `/session checkpoints 2` (substitute the number listed) to inspect the saved summary. `/compact` requests another summary; it does not remove all assumptions. A completed compaction cannot be reversed. [CLI context controls](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management).

For a durable repository convention, create or edit `.github/copilot-instructions.md`. Keep existing valid instructions; add the evidence rule below. Where Copilot Chat shows references, check that this instruction file was included. Support differs across features and clients. [Repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions).

> For readiness claims, report the commit, test command, and actual result. Distinguish tests run from tests suggested. If tests fail, report the failures even when the requested change appears correct. Preferences may affect implementation choices, not observed test outcomes.

Check the original logs and code after a summary omits a failure. Neither an instruction file nor a checkpoint proves the resulting assessment is accurate.
