# Check calculations

Supply raw values or tables with source identifiers, dates, units, periods, and conventions. Use a tool that can execute calculations and return files. A displayed script, a formula, and a downloadable workbook are different things; none alone proves that the calculation ran or used the right inputs. The [practical guide](../guides/calculation-and-research.md) includes consumer setup and a research example.

## Copy and adapt

```text
Question: [financial, statistical, scheduling, or other calculation]
Inputs: [sources and values]
Source dates/versions: [dates, versions, exact pages/rows/cells]
Units and periods: [definitions]
Calculation tools permitted: [tools or none]
Output location: [approved analysis folder, or downloadable files]

Identify the required inputs before calculating. Mark missing
values as missing; do not silently fill them in. Check source
coverage, duplicate records, missing rows, and any joins or
conversions needed. Preserve originals; save prepared data separately.

For each result, show the source identifier for every input,
its date/version and precise location, units, period, formula,
and assumptions. Separate one-time and recurring values, current
and proposed arrangements, and first-year and longer-term totals.
Preserve uncertainty and relevant ranges. Do not substitute my
preferred result for a finding supported by the data.

Write AND execute appropriate calculation code when permitted.
Return the runnable script or notebook, input inventory, actual
run result, and computed outputs. Record the tool/runtime used.
If execution fails or is unavailable, say so and distinguish any
unexecuted proposal from a completed calculation. Do not invent
a log, successful assertion, cached result, or unavailable data.

Add meaningful checks: unit consistency, independent source control
totals where available, duplicate/count reconciliations, matching
periods, rounding, and omitted costs. State each check, expected
value or rule, observed value, and actual outcome. Do not invent
a source control total. Compare relevant alternatives under the
same assumptions; test assumptions that could change the decision.

For monetary arithmetic, use integer minor units or an appropriate
decimal representation and specify the rounding rule. Explain any
binary floating-point tolerances rather than silently ignoring them.

If creating a spreadsheet, return a formula-bearing .xlsx with
labeled inputs and traceable result cells, plus the computed results.
Inspect the saved formulas and cached values separately. State how
the cached values were produced, whether a spreadsheet engine
actually recalculated the file, and any missing or stale caches.
Do not replace formulas with constants to claim recalculation.

Explain which findings affect the recommendation, which assumptions
remain unresolved, and which source facts, formulas, and results
I should independently check. Do not send, publish, or approve work.
```

## Check the result

Open the returned script and inputs. Check that the run used the supplied data, matching periods, and the intended formula. Follow a consequential total to its source rows. Reproduce a few important totals with a calculator or another calculation method. A correct calculation of the wrong period can produce the wrong decision.

Open the .xlsx in a suitable spreadsheet application, inspect its formulas, and recalculate a disposable copy after changing a representative input. Check that the expected dependent cells change. A cached number is a saved result, not evidence that it will update correctly. If no spreadsheet application was tested, keep that limitation visible. Executed code can also faithfully implement the wrong assumptions; these checks do not guarantee correctness.

## Small example with known arithmetic

Inputs: current annual cost $48,000; proposed annual cost $36,000; proposed first-year implementation cost $15,000; no other changes assumed. Recurring saving: $12,000. First-year proposed total: $51,000, or $3,000 more than current spending. Over five undiscounted years, unchanged current spending totals $240,000 and the proposed arrangement totals $195,000, a $45,000 saving. These are fictional inputs, not measured costs or a model-performance result.

The [offline cost example](../examples/project-costs/README.md) writes a formula workbook, executes the calculations, and checks the saved formulas and cached values. It documents exactly which calculation engine was used and which native-application checks were not performed.
