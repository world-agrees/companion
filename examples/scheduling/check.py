"""Calculate the fictional Chapter 8 example without an LLM or network call."""
import csv
from decimal import Decimal
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
with (HERE / 'task-list.csv').open(newline='') as source:
    tasks = list(csv.DictReader(source))
hours = [Decimal(task['estimated_hours']) for task in tasks]
if any(not value.is_finite() or value < 0 for value in hours):
    raise ValueError('Estimates must be finite and nonnegative')
availability = (HERE / 'availability.txt').read_text()
match = re.search(r'Hours available before Friday: (\d+(?:\.\d+)?)', availability)
if match is None:
    raise ValueError('No available-hours figure found')
work = sum(hours, Decimal('0'))
available = Decimal(match.group(1))
print(f'Estimated work: {work} hours')
print(f'Available time: {available} hours')
print(f'Shortfall: {max(work - available, Decimal("0"))} hours')
print('Basis: one person, sequential tasks; estimates are not measured durations.')
