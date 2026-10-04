# An offline project-cost calculation

Open the included [project-costs.xlsx](project-costs.xlsx) without running code. Its **fictional** inputs come from Chapter 9: $48,000 per year for the current arrangement, $36,000 per year for the proposed arrangement, and $15,000 for implementation in year one. They are not supplier quotes, observed spending, or a purchasing recommendation. [results.csv](results.csv) and [verification.json](verification.json) provide the calculated totals and executed checks.

The runnable script makes no network or API calls. It writes a formula-bearing workbook and its results to a new temporary directory, preserving this source directory.

## Run it if you want to inspect or reproduce the calculation

Use Python 3.10 or later with **xlsxwriter** and **openpyxl** available in an approved environment. The script does not install dependencies. In an assistant's existing calculation environment, supply this script and ask it to execute the file and return its outputs. Displaying the code is not a completed run.

From this directory:

```sh
python3 project_costs.py
```

Or choose a new or empty temporary output directory:

```sh
python3 project_costs.py --output-dir /tmp/world-agrees-cost-review
```

The script prints the output directory and actual check counts. It refuses to overwrite a nonempty directory or write inside **reader-resources/**. The workbook uses fixed example metadata. The verification record reports the actual execution time, library versions, and workbook hash without personal runtime paths.

## What the example checks

| Finding | Expected amount |
| --- | ---: |
| Recurring annual saving | $12,000 |
| First-year proposed cost | $51,000 |
| First-year additional cost | $3,000 |
| Five-year current cost | $240,000 |
| Five-year proposed cost | $195,000 |
| Five-year saving | $45,000 |

The annual rate remains unchanged over five undiscounted years. Implementation occurs once, in year one. No other costs, inflation, taxes, financing, or savings are assumed. Those exclusions are assumptions of this fictional example, not conclusions about a real project.

The script uses **Decimal** for exact USD arithmetic and rejects missing, nonfinite, negative, or fractional-cent inputs for this example. It checks the known totals, their reconciliation to the yearly schedule, a zero implementation cost, a higher implementation cost that reverses the five-year conclusion, and preservation of cents. It reopens the saved workbook with openpyxl twice: once for formula text and once for cached values. It checks saved inputs and recomputes each declared formula before comparing its cache. The verification record includes check outcomes and the important summary cells.

## What a formula cache means here

The caches were produced by the script's executed, restricted Python evaluator and supplied to xlsxwriter alongside the formulas. That evaluator handles only the explicit arithmetic used here. It is not a general Excel engine. openpyxl inspects workbook contents; it does not calculate formulas.

The distributed workbook was also recalculated and visually inspected with **@oai/artifact-tool**. Its six summary results matched the known baseline. Changing the proposed annual cost to $40,000 produced the expected $25,000 five-year saving; restoring $36,000 restored the $45,000 result. The formula-error scan found no matches. These additional checks are recorded separately in the included verification report; the Python script does not claim to rerun them.

**The script does not run Excel or LibreOffice.** Its report states that native-application recalculation was not performed. The workbook requests automatic recalculation when opened, but that setting is not proof that your application recalculated it. After changing an input, recalculate a disposable copy in your spreadsheet application and confirm the dependent totals change. Inspect the inputs yourself: spreadsheet applications can treat blanks as zero, making a missing source cost look harmless.

For a simple sanity check, add $36,000 and $15,000 with a calculator, then compare that $51,000 first-year cost with $48,000. For five years, calculate $36,000 × 5 + $15,000 and compare it with $48,000 × 5. Check the assumptions before applying the formulas to real data. Correct arithmetic cannot establish that every cost or condition has been included.

Use the [calculation prompt](../../prompts/03-check-calculations.md) and [practical calculation/research guide](../../guides/calculation-and-research.md) to adapt the method to your own inspected sources.
