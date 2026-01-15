#!/usr/bin/env python3
"""
Test search logic
"""
import sys
sys.path.insert(0, '.')

from database.db import Database
from models.case import Case

db = Database()
cases = db.get_all_cases()
print(f"Total casos en BD: {len(cases)}")

# Convert to Case objects
case_objects = [Case.from_row(c) for c in cases]
print(f"Casos convertidos: {len(case_objects)}")

# Test simple filter
query = ''
selected_cat = 'Todas'

def matches(case):
    text_match = query in str(vars(case)).lower()
    cat_match = True  # "Todas"
    return text_match and cat_match

filtered = [c for c in case_objects if matches(c)]
print(f"Casos filtrados con 'Todas': {len(filtered)}")

# Show first 5
for i, case in enumerate(filtered[:5]):
    print(f"  {i+1}. ID {case.id}: {case.numero_carpeta} - {case.categoria}")
