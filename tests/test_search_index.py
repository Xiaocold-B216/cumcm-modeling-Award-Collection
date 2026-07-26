# -*- coding: utf-8 -*-
import json
from pathlib import Path

def test_search_index_exists():
    assert Path('analysis-index/12_search/search_index.json').exists()

def test_search_index_structure():
    with open('analysis-index/12_search/search_index.json', 'r', encoding='utf-8') as f:
        index = json.load(f)
    assert 'schema_version' in index
    assert 'total_documents' in index
    assert 'total_concepts' in index
    assert 'documents' in index
    assert 'concept_index' in index
    assert 'keyword_index' in index

def test_search_index_has_documents():
    with open('analysis-index/12_search/search_index.json', 'r', encoding='utf-8') as f:
        index = json.load(f)
    assert index['total_documents'] > 0
    assert len(index['documents']) > 0

def test_search_index_has_concepts():
    with open('analysis-index/12_search/search_index.json', 'r', encoding='utf-8') as f:
        index = json.load(f)
    assert index['total_concepts'] > 0
    assert len(index['concept_index']) > 0
