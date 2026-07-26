# -*- coding: utf-8 -*-
import json
from pathlib import Path

def test_normalization_registry_exists():
    assert Path('analysis-index/10_normalization/concept_registry.json').exists()

def test_normalization_registry_structure():
    with open('analysis-index/10_normalization/concept_registry.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)
    assert 'schema_version' in registry
    assert 'total_methods' in registry
    assert 'normalized_concepts' in registry
    assert len(registry['normalized_concepts']) > 0

def test_concept_has_required_fields():
    with open('analysis-index/10_normalization/concept_registry.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)
    for concept in registry['normalized_concepts'][:10]:
        assert 'concept_id' in concept
        assert 'canonical_name' in concept
        assert 'frequency' in concept
        assert 'years' in concept
