# Ask for executed calculations and inspectable research

You can ask a consumer assistant to analyze files without becoming a programmer. The useful request is more specific than “check my numbers”: identify the inputs, write and execute the calculation, return the work, and explain what remains uncertain. You still need to check whether the sources and assumptions describe the decision you are making.

## Set up a consumer calculation

These product directions were checked against official documentation on October 3, 2026. Availability depends on your account, client, and organization.

For **Claude on the web or desktop**:

1. Open **Settings → Capabilities** and check **Code execution and file creation**. Organization owners can control this capability for Team and Enterprise accounts. You do not need Claude Code for this workflow. [Claude's file-creation documentation](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)
2. Attach the source files and manifest. XLSX upload requires that capability; use a supported readable export when a source cannot be processed, and record what the export omits. [Claude's upload documentation](https://support.claude.com/en/articles/8241126-upload-files-to-claude)
3. Paste the [calculation prompt](../prompts/03-check-calculations.md). Explicitly ask it to **write and execute** code, then provide the runnable script, input record, computed results, and formula-bearing .xlsx.
4. Download and inspect the returned work. If execution was unavailable or failed, keep the result labeled unexecuted rather than accepting a plausible-looking number as a successful run.

Use a chat where the capability is available. In the new Claude experience, incognito opens the previous interface, which cannot create files or run code. Use the appropriate context controls for the supported calculation workflow. [Claude's interface documentation](https://support.claude.com/en/articles/16761823-claude-cowork-and-chat-are-one-claude)

For **ChatGPT Work**:

ChatGPT Work is unavailable in a project using project-only memory. Start a separate task and inspect its environment, attached folders, plugins, sources, and standing context. These access controls do not establish the same memory boundary; a fresh Work task can still use applicable personal context. [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), [Work capabilities](https://learn.chatgpt.com/docs/use-chatgpt).

1. Select **Work** in the web or desktop interface and start the task in the approved workspace. Attach the CSVs or Excel workbooks and the source manifest. You do not need to set up local Python before analyzing attached files. [OpenAI's dataset workflow](https://learn.chatgpt.com/use-cases/datasets-and-reports)
2. Paste the same calculation prompt, specifying the decision, units, periods, permitted tools, and outputs. Request the code and actual execution result as well as the answer.
3. Open the generated files in the chat and download them for review. Name the sheet, cell, or other location when requesting a correction, and ask what checks were actually repeated. [OpenAI's file workflow](https://learn.chatgpt.com/docs/artifacts-viewer)

A folder path in a prompt does not give either product local filesystem access. For attachment-based work, supply the selected files explicitly. For a supported local-folder workflow, inspect its granted permissions. Keep source records unchanged and save derived data, scripts, and workbooks in the project's **analysis/** folder.

## Distinguish a calculation from its explanation

Ask for an input table with source IDs, dates and versions, values, units, periods, and exact source locations. Missing data should remain missing. If a source gives annual spending, the model must not quietly compare it with a monthly subscription or a total covering several years.

Request the runnable code and the actual run result. A code block can contain a good proposed calculation without ever having been executed. A successful run can also implement the wrong formula. Check that the code ran and that it calculated the comparison you intended.

Ask for checks that could catch a wrong result: missing or duplicate records, mismatched units or periods, and disagreement with a total already reported in the source. The assistant should not invent a source total or call a check successful merely because it suggested one. Ask which assumptions could reverse the recommendation and compare realistic alternatives under the same assumptions.

For money, ask for decimal arithmetic or integer cents with a stated rounding rule. A formatted currency cell can conceal rounding or a floating-point discrepancy. Formatting changes what you see; it does not repair the underlying calculation.

## Ask for formulas and saved results separately

A formula-bearing workbook lets you trace a result to its input cells. A cached value is the result saved alongside a formula so a viewer can display it without recalculating. The cache may be missing or stale. Neither a formula nor its cache proves that the workbook will respond correctly to a changed input.

Ask which engine computed the saved results: an executed Python calculation, a spreadsheet application, or another supported calculation tool. If Python computed caches for the bundled example's formulas, that is different from Excel recalculating the workbook. Have the assistant identify what was executed and what was not tested.

Open the returned workbook. Inspect an important result's formula and source cells. In a disposable copy, change an input and recalculate in your spreadsheet application. Check the expected dependent results. Separately reproduce important arithmetic yourself and examine the exclusions: tax, installation, maintenance, timing, and other relevant costs. Do not add a cost simply because this list mentions it; establish whether it applies.

The [offline project-cost example](../examples/project-costs/README.md) illustrates the book's fictional $48,000, $36,000, and $15,000 inputs. It creates a formula workbook and a verification record, with no network access. Its README distinguishes executed checks from native Excel or LibreOffice tests.

## Research before plotting: a car-price example

The same discipline applies when the inputs come from research. A chart can look authoritative even when it combines asking prices, reported sale prices, different trims, and observations taken years apart.

Define the vehicle and the comparison before asking for a trend. Keep the seller's asking price separate from a documented transaction price. A listing marked “sold” does not by itself establish what the buyer paid. Record the currency, mileage, trim, condition, location, source, relevant dates, and fees included or excluded. If historical records are unavailable, report the gap rather than inventing a smooth series.

Access can determine the usable period. eBay distinguishes recent completed-listing searches covering 90 days from Seller Hub Product research covering up to three years. Its documentation does not guarantee a complete vehicle-price series for your search or account. Record the period and records you can actually inspect. An ended listing is not proof of a sale, and the price displayed may differ from an accepted offer. [eBay Product research](https://www.ebay.com/help/selling/selling-tools/product-research?id=4853)

Copy and adapt:

```text
Question: [car-price comparison or historical trend]
Vehicle: [make, model, model years, trim, drivetrain]
Scope: [location, mileage/condition range, date range, currency]
Sources permitted: [public primary seller/auction records,
authorized supplied records, and other expressly permitted sources]
Outputs: [approved analysis folder, or downloadable files]

First inventory the available sources and propose a collection plan.
Do not report price findings until you have inspected the records.
Use original listing or auction-result pages where available.
Identify access, licensing, extraction, and historical coverage limits.
Do not bypass access controls or invent unavailable observations.

Build a source-backed dataset. Give each observation a stable ID,
source URL or supplied-file ID, date retrieved, listing/result date
if known, vehicle details, amount, currency, price type, and any
included fees. Preserve the reported amount before conversions.
Separate asking prices, documented sale prices, unsold lots, and
unknown transaction prices. A sold status is not a sale price.
Do not infer a final price from an earlier asking price.

Save the observations as CSV and a source manifest. Retain permitted
source extracts or snapshots where possible, with their IDs and
dates. Record cleaning, exclusions, duplicates, and missing fields
in a separate preparation log. Do not replace originals with summaries.

Before estimating a trend, explain which records are comparable and
which are not. Keep currencies, price types, and materially different
vehicle categories separate unless an explicitly documented method
justifies combining them. Label nominal versus adjusted prices and
any external adjustment inputs. Do not guess missing historical data.

Write AND execute analysis and plotting code using the inspected
dataset. Report the runtime, actual run output, record counts,
date coverage, and checks. Return the runnable script, prepared
dataset, computed summaries, chart, and source manifest. Identify
unexecuted steps or failed checks honestly.

Use labels that disclose price type, currency, period, and sample
size. Show individual observations or appropriate summaries without
suggesting continuous coverage where records are missing. Do not
invent points or connect gaps as though prices were observed there.
Explain sampling limits and changes in vehicle mix that could
explain a trend. Do not present this sample as the entire market.

State what the records support, what remains unknown, and what
I should check before relying on the result. Do not buy, bid,
contact sellers, or send anything.
```

Inspect several source rows yourself, including a value that strongly affects the chart. Check that the plotting code used the supplied dataset rather than a sample it generated. Save the dataset and analysis version with the chart so another person can reproduce the result. This prompt is a research procedure, not a completed price study or a purchasing recommendation.

## Share the procedure as well as the document

A team can keep approved prompts in its project alongside source records and analysis. Give each procedure an owner, date, version, stage, and required outputs. Use the [document-project instructions template](../templates/document-project-instructions.md) to identify exactly which procedure governs a task and who checks the result.

In a consumer chat, paste or upload the selected procedure, or place the appropriate instructions in the product's supported project settings. Ask the assistant to identify the version it could actually read. Merely placing Markdown files in a **prompts/** directory does not mean they were loaded, and an assistant's claim is still something to compare with the supplied files. Automatic instruction-file discovery is a product capability, not a property of Markdown.

Keep the outcome you hope for out of the assessment inputs. Supply the audience, decision question, and criteria. Then use the [evidence workflow](../prompts/14-evidence-workflow.md) to move from inventory to checked analysis and drafting. A shared procedure makes the checks repeatable; it does not enforce permissions, retrain the model, or guarantee that the output is correct.
