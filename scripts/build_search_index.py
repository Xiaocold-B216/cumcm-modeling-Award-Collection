# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path
from collections import defaultdict

def build_search_index():
    '''Build a local search index for the CUMCM corpus'''
    
    # Load concept registry
    with open('analysis-index/10_normalization/concept_registry.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    # Collect all documents
    documents = []
    doc_years = range(1992, 2026)
    
    for year in doc_years:
        # Load logical documents
        doc_file = Path(f'analysis-index/02_documents/logical_documents/{year}.csv')
        if doc_file.exists():
            import csv
            with open(doc_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['year'] = year
                    documents.append(row)
    
    print(f'Collected {len(documents)} documents')
    
    # Build inverted index
    index = {
        'schema_version': '1.0.0',
        'created_at': '2026-07-26',
        'total_documents': len(documents),
        'total_concepts': len(registry['normalized_concepts']),
        'documents': [],
        'concept_index': {},
        'keyword_index': defaultdict(list)
    }
    
    # Index documents
    for doc in documents:
        doc_id = doc.get('logical_document_id', doc.get('document_id', ''))
        if not doc_id:
            continue
        
        doc_entry = {
            'document_id': doc_id,
            'year': doc.get('year'),
            'role': doc.get('role', doc.get('document_role', 'unknown')),
            'title': doc.get('title', ''),
            'problem_id': doc.get('problem_id', ''),
            'keywords': []
        }
        
        # Extract keywords from title and other fields
        title = doc_entry['title']
        if title:
            # Simple keyword extraction (split by common delimiters)
            keywords = set()
            for word in title.replace(',', ' ').replace('，', ' ').replace('、', ' ').split():
                if len(word) >= 2:
                    keywords.add(word.lower())
            doc_entry['keywords'] = list(keywords)
            
            # Add to keyword index
            for kw in keywords:
                index['keyword_index'][kw].append(doc_id)
        
        index['documents'].append(doc_entry)
    
    # Index concepts
    for concept in registry['normalized_concepts']:
        concept_id = concept['concept_id']
        index['concept_index'][concept_id] = {
            'canonical_name': concept['canonical_name'],
            'frequency': concept['frequency'],
            'years': concept['years'],
            'documents': concept['documents']
        }
    
    # Convert defaultdict to regular dict for JSON serialization
    index['keyword_index'] = dict(index['keyword_index'])
    
    # Save index
    os.makedirs('analysis-index/12_search', exist_ok=True)
    with open('analysis-index/12_search/search_index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f'Search index created:')
    print(f'  Documents: {index["total_documents"]}')
    print(f'  Concepts: {index["total_concepts"]}')
    print(f'  Keywords: {len(index["keyword_index"])}')
    
    return index

if __name__ == '__main__':
    build_search_index()
