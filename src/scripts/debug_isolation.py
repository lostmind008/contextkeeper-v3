#!/usr/bin/env python3
"""Debug script to understand the vector search cross-contamination issue"""

import requests
import json
import chromadb
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect directly to ChromaDB
DB_PATH = ".chromadb"
client = chromadb.PersistentClient(path=DB_PATH)

def inspect_collections():
    """Inspect all collections in ChromaDB"""
    logger.info("=== ChromaDB Collections ===")
    collections = client.list_collections()
    
    for collection in collections:
        logger.info(f"\nCollection: {collection.name}")
        logger.info(f"  Metadata: {collection.metadata}")
        
        # Get all items
        try:
            results = collection.get()
            logger.info(f"  Total items: {len(results['ids'])}")
            
            # Check project_id metadata
            if results['metadatas']:
                project_ids = set()
                for metadata in results['metadatas']:
                    if 'project_id' in metadata:
                        project_ids.add(metadata['project_id'])
                logger.info(f"  Unique project_ids in collection: {project_ids}")
                
                # Sample some documents
                for i in range(min(3, len(results['ids']))):
                    logger.info(f"\n  Sample {i+1}:")
                    logger.info(f"    ID: {results['ids'][i]}")
                    logger.info(f"    Metadata: {results['metadatas'][i]}")
                    logger.info(f"    Content preview: {results['documents'][i][:100]}...")
        except Exception as e:
            logger.error(f"  Error reading collection: {e}")

def test_direct_query():
    """Test querying directly via ChromaDB"""
    logger.info("\n=== Direct ChromaDB Query Test ===")
    
    # Find all collections
    collections = client.list_collections()
    logger.info(f"Total collections: {len(collections)}")
    
    for collection in collections:
        logger.info(f"\nQuerying collection: {collection.name}")
        
        # Query for ALPHA-UNIQUE
        results = collection.query(
            query_texts=["ALPHA-UNIQUE-12345"],
            n_results=3
        )
        
        logger.info(f"Results for 'ALPHA-UNIQUE-12345':")
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                logger.info(f"  - Distance: {results['distances'][0][i]}")
                logger.info(f"    Metadata: {results['metadatas'][0][i]}")
                logger.info(f"    Content preview: {results['documents'][0][i][:100]}...")

if __name__ == "__main__":
    inspect_collections()
    test_direct_query()