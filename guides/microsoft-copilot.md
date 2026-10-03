# Microsoft Copilot: distinguish the consumer and workplace controls

Documentation checked **October 2, 2026**. Begin by identifying the product and signed-in account. Consumer Copilot, Microsoft 365 Copilot, and GitHub Copilot are different products. This guide covers the first two; GitHub Copilot belongs in the coding-assistant guide.

## Consumer Copilot: inspect and limit personalization

1. Open **Settings → Personalization**.
2. Beside **Saved memories**, select **Manage** and remove the relevant item.
3. Turn saved memory off if you want to stop further saving; existing items require deletion separately.
4. Review **One shared experience** and **Web search** independently.

The updated app uses these controls. Microsoft's older privacy-controls page applies to versions before the August 18, 2026 update. [Current consumer controls](https://support.microsoft.com/en-us/privacy/microsoft-copilot/privacy-controls), [legacy-version notice](https://support.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-privacy-controls)

Delete an unwanted conversation separately: on the web, open its three-dot menu and choose the deletion action; desktop and mobile use their documented history menus. [Conversation-history controls](https://support.microsoft.com/en-us/microsoft-copilot/conversation-history-in-microsoft-copilot)

Verification: reopen the memory list and confirm the relevant item is absent. Keep the source and your correction outside the chat. Do not assume a memory switch has also deleted history, disabled web search, or changed advertising choices.

## Microsoft 365 Copilot: inspect separate memory layers

Open **••• Settings and more → Chat settings → Personalization**. Use **Manage saved memories** to remove a specific item; the saved-memory switch and deletion are separate. [Saved-memory instructions](https://support.microsoft.com/en-us/microsoft-365-copilot/manage-copilot-memory-in-microsoft-365-copilot)

Review **Chat history**, or **Chat history & work insights** for the applicable work account. Turning this off schedules deletion of the corresponding inferences after thirty days. Switching it back on during that period restores them. [Chat-history personalization](https://support.microsoft.com/en-us/microsoft-365-copilot/how-microsoft-365-copilot-chat-history-works)

For a single conversation, use the temporary-chat button at the top right. This avoids personalized memory use and updates, stays out of your visible history, and remains subject to organizational retention. [Temporary-chat instructions](https://support.microsoft.com/en-us/microsoft-365-copilot/personalize-what-microsoft-365-copilot-remembers)

Where available, the **Work IQ** button at the top left controls Microsoft 365 work-data grounding. Turning it off still allows supplied attachments, web information, and user personalization as inputs. [Work-data controls](https://support.microsoft.com/en-us/microsoft-365-copilot/what-information-does-copilot-use-to-answer-my-prompt)

Verification: note the selected source controls and inspect the actual document citations. None provides a complete view of the service's assembled model input. If a workplace policy fixes the controls, obtain the relevant configuration from the administrator rather than infer it from a reply.

## Give the model an inspectable task

When drafting a status report, supply the actual plan, dated changes, test results, and capacity estimates. Avoid giving it only an optimistic executive summary.

> Prepare a status assessment from [named, dated sources]. First list each commitment, its conditions, and supporting source location. Compare actual progress with the agreed criteria. Separate verified results from estimates and missing data. Keep conditions and failed checks in the summary. Identify conflicting documents and ask which version governs. Do not improve the reported status to match the audience's preferences.

Verification: check the commitment that matters. “Friday, if another assignment is removed” must not become an unconditional Friday promise. Open the source and read the surrounding condition.

## Test a changed answer

> Identify what new evidence changed your recommendation after my objection. If the evidence did not change, repeat the assessment against the same criteria. Do not treat my dissatisfaction as a new project fact.

If a model changes a conclusion after you add a new test result, check that result. If it changes after you merely ask for a more positive summary, compare which facts or conditions disappeared. You are checking the work, not asking the software for a confession.

Store a compact review record: sources and dates, active controls, correction made, output, decisive claim checked, and remaining uncertainty. Repeat the check when you change the evidence or settings, rather than keep requesting agreement. These prompts request a behavior; they do not establish an enforced source boundary or guarantee against sycophancy.
