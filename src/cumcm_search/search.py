# -*- coding: utf-8 -*-
import json
from pathlib import Path

def load_index(index_path='analysis-index/12_search/search_index.json'):
    '''Load the search index'''
    with open(index_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_corpus(query, index=None, index_path='analysis-index/12_search/search_index.json'):
    '''Search the CUMCM corpus'''
    if index is None:
        index = load_index(index_path)
    
    results = []
    query_lower = query.lower()
    
    for doc in index['documents']:
        score = 0
        matched_keywords = []
        
        if query_lower in doc.get('title', '').lower():
            score += 10
            matched_keywords.append('title')
        
        for kw in doc.get('keywords', []):
            if query_lower in kw or kw in query_lower:
                score += 5
                matched_keywords.append(kw)
        
        if query_lower in doc.get('problem_id', '').lower():
            score += 3
            matched_keywords.append('problem_id')
        
        if score > 0:
            results.append({
                'document_id': doc['document_id'],
                'year': doc['year'],
                'role': doc['role'],
                'title': doc['title'],
                'score': score,
                'matched_keywords': matched_keywords
            })
    
    concept_results = []
    for concept_id, concept in index.get('concept_index', {}).items():
        if query_lower in concept['canonical_name'].lower():
            concept_results.append({
                'concept_id': concept_id,
                'canonical_name': concept['canonical_name'],
                'frequency': concept['frequency'],
                'years': concept['years']
            })
    
    results.sort(key=lambda x: -x['score'])
    
    return {
        'query': query,
        'document_results': results[:20],
        'concept_results': concept_results[:10],
        'total_matches': len(results)
    }
