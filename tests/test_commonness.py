# -*- coding: utf-8 -*-
import json
from pathlib import Path

def test_commonness_grading_exists():
    assert Path('analysis-index/11_commonness/commonness_grading.json').exists()

def test_commonness_grading_structure():
    with open('analysis-index/11_commonness/commonness_grading.json', 'r', encoding='utf-8') as f:
        grading = json.load(f)
    assert 'schema_version' in grading
    assert 'levels' in grading
    assert 'statistics' in grading
    assert all(level in grading['levels'] for level in ['very_common', 'common', 'moderate', 'rare'])

def test_commonness_statistics_sum():
    with open('analysis-index/11_commonness/commonness_grading.json', 'r', encoding='utf-8') as f:
        grading = json.load(f)
    total = sum(s['count'] for s in grading['statistics'].values())
    assert total == grading['total_concepts']
