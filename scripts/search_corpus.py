# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

def search_corpus(query, index_path='analysis-index/12_search/search_index.json'):
    '''Search the CUMCM corpus'''
    
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    results = []
    query_lower = query.lower()
    
    # Search in keywords
    for doc in index['documents']:
        score = 0
        matched_keywords = []
        
        # Check title match
        if query_lower in doc.get('title', '').lower():
            score += 10
            matched_keywords.append('title')
        
        # Check keyword match
        for kw in doc.get('keywords', []):
            if query_lower in kw or kw in query_lower:
                score += 5
                matched_keywords.append(kw)
        
        # Check problem_id match
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
    
    # Search in concepts
    concept_results = []
    for concept_id, concept in index['concept_index'].items():
        if query_lower in concept['canonical_name'].lower():
            concept_results.append({
                'concept_id': concept_id,
                'canonical_name': concept['canonical_name'],
                'frequency': concept['frequency'],
                'years': concept['years']
            })
    
    # Sort results by score
    results.sort(key=lambda x: -x['score'])
    
    return {
        'query': query,
        'document_results': results[:20],
        'concept_results': concept_results[:10],
        'total_matches': len(results)
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python search_corpus.py <query>')
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    results = search_corpus(query)
    
    print(f'Search results for: {query}')
    print(f'Total matches: {results["total_matches"]}')
    
    if results['document_results']:
        print('\nDocument results:')
        for i, doc in enumerate(results['document_results'][:5], 1):
            print(f'  {i}. [{doc["year"]}] {doc["title"]} (score: {doc["score"]})')
    
    if results['concept_results']:
        print('\nConcept results:')
        for i, concept in enumerate(results['concept_results'][:5], 1):
            print(f'  {i}. {concept["canonical_name"]} (frequency: {concept["frequency"]})')
