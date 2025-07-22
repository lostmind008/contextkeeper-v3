#!/usr/bin/env python3
"""
RAG Knowledge Agent for Project Memory
Maintains persistent knowledge across coding sessions
Author: YouTube Analyzer Project
Date: July 2025
"""

import os
import re
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
import hashlib
import argparse

# Core dependencies
import chromadb
from chromadb.config import Settings
from google import genai
from google.genai.types import HttpOptions
import tiktoken
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rag_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    "db_path": "./rag_knowledge_db",
    "watch_dirs": [
        "/Users/sumitm1/Documents/myproject/Ongoing Projects/LostMindAI - Youtube Analyser Tool/agents",
        "/Users/sumitm1/Documents/myproject/Ongoing Projects/LostMindAI - Youtube Analyser Tool/backend",
        "/Users/sumitm1/Documents/myproject/Ongoing Projects/LostMindAI - Youtube Analyser Tool/tools"
    ],
    "file_extensions": [".py", ".js", ".jsx", ".ts", ".tsx", ".md", ".json", ".yaml"],
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "max_results": 10,
    "embedding_model": "text-embedding-004",
    "api_port": 5555,
    "sensitive_patterns": [
        r'api[_-]?key\s*[:=]\s*["\']([^"\']+)["\']',
        r'password\s*[:=]\s*["\']([^"\']+)["\']',
        r'secret\s*[:=]\s*["\']([^"\']+)["\']',
        r'token\s*[:=]\s*["\']([^"\']+)["\']',
        r'stripe[_-]?key\s*[:=]\s*["\']([^"\']+)["\']'
    ]
}

class SecurityFilter:
    """Filters sensitive information before embedding"""
    
    def __init__(self, patterns: List[str]):
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
    
    def clean(self, content: str) -> str:
        """Remove sensitive data from content"""
        cleaned = content
        for pattern in self.patterns:
            cleaned = pattern.sub('[REDACTED]', cleaned)
        return cleaned

class TextChunker:
    """Intelligent text chunking for code and documentation"""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.encoding = tiktoken.encoding_for_model("gpt-4")
    
    def chunk_code(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Create semantic chunks from code files"""
        chunks = []
        lines = content.split('\n')
        
        # Try to chunk by functions/classes for code files
        if file_path.endswith(('.py', '.js', '.ts')):
            chunks = self._chunk_by_structure(lines, file_path)
        else:
            chunks = self._chunk_by_size(content, file_path)
        
        return chunks
    
    def _chunk_by_structure(self, lines: List[str], file_path: str) -> List[Dict[str, Any]]:
        """Chunk code by structural boundaries"""
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for i, line in enumerate(lines):
            tokens = len(self.encoding.encode(line))
            
            # Detect structural boundaries
            is_boundary = (
                line.strip().startswith(('def ', 'class ', 'function ', 'const ', 'export ')) or
                (current_tokens + tokens > self.chunk_size and len(current_chunk) > 10)
            )
            
            if is_boundary and current_chunk:
                # Save current chunk
                chunk_text = '\n'.join(current_chunk)
                chunks.append({
                    'content': chunk_text,
                    'metadata': {
                        'file': file_path,
                        'start_line': i - len(current_chunk),
                        'end_line': i - 1,
                        'type': 'code',
                        'tokens': current_tokens
                    }
                })
                
                # Start new chunk with overlap
                overlap_lines = max(0, len(current_chunk) - 5)
                current_chunk = current_chunk[-5:] if overlap_lines > 0 else []
                current_tokens = sum(len(self.encoding.encode(l)) for l in current_chunk)
            
            current_chunk.append(line)
            current_tokens += tokens
        
        # Don't forget the last chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append({
                'content': chunk_text,
                'metadata': {
                    'file': file_path,
                    'start_line': len(lines) - len(current_chunk),
                    'end_line': len(lines) - 1,
                    'type': 'code',
                    'tokens': current_tokens
                }
            })
        
        return chunks
    
    def _chunk_by_size(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Simple size-based chunking for non-code files"""
        chunks = []
        tokens = self.encoding.encode(content)
        
        for i in range(0, len(tokens), self.chunk_size - self.overlap):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            chunks.append({
                'content': chunk_text,
                'metadata': {
                    'file': file_path,
                    'chunk_index': i // (self.chunk_size - self.overlap),
                    'type': 'document',
                    'tokens': len(chunk_tokens)
                }
            })
        
        return chunks

class ProjectKnowledgeAgent:
    """Main RAG agent for project knowledge management"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.security_filter = SecurityFilter(config['sensitive_patterns'])
        self.chunker = TextChunker(config['chunk_size'], config['chunk_overlap'])
        
        # Initialize Google GenAI
        try:
            self.embedder = genai.Client(
                http_options=HttpOptions(api_version="v1")
            )
            logger.info("Google GenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize GenAI client: {e}")
            raise
        
        # Initialize ChromaDB
        self.db = chromadb.PersistentClient(
            path=config['db_path'],
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Create or get collection
        try:
            self.collection = self.db.get_collection("project_knowledge")
            logger.info("Using existing ChromaDB collection")
        except:
            self.collection = self.db.create_collection(
                name="project_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Created new ChromaDB collection")
        
        # Track processed files
        self.processed_files = self._load_processed_files()
    
    def _load_processed_files(self) -> Dict[str, str]:
        """Load hash of previously processed files"""
        hash_file = Path(self.config['db_path']) / "processed_files.json"
        if hash_file.exists():
            with open(hash_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_processed_files(self):
        """Save hash of processed files"""
        hash_file = Path(self.config['db_path']) / "processed_files.json"
        with open(hash_file, 'w') as f:
            json.dump(self.processed_files, f, indent=2)
    
    def _get_file_hash(self, file_path: str) -> str:
        """Calculate file hash for change detection"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embeddings using Google's text-embedding-004"""
        try:
            response = await asyncio.to_thread(
                self.embedder.models.embed_content,
                model=self.config['embedding_model'],
                contents=text
            )
            return response.embeddings[0].values
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            raise
    
    async def ingest_file(self, file_path: str) -> int:
        """Process and embed a single file"""
        try:
            # Check if file needs processing
            current_hash = self._get_file_hash(file_path)
            if (file_path in self.processed_files and 
                self.processed_files[file_path] == current_hash):
                logger.debug(f"Skipping unchanged file: {file_path}")
                return 0
            
            # Read and clean content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cleaned_content = self.security_filter.clean(content)
            
            # Chunk the content
            chunks = self.chunker.chunk_code(cleaned_content, file_path)
            
            # Embed and store each chunk
            chunk_count = 0
            for chunk in chunks:
                embedding = await self.embed_text(chunk['content'])
                
                # Generate unique ID
                chunk_id = f"{file_path}_{chunk['metadata'].get('chunk_index', chunk['metadata'].get('start_line', 0))}"
                
                # Store in ChromaDB
                self.collection.upsert(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    documents=[chunk['content']],
                    metadatas=[{
                        **chunk['metadata'],
                        'ingested_at': datetime.now().isoformat()
                    }]
                )
                chunk_count += 1
            
            # Update processed files
            self.processed_files[file_path] = current_hash
            self._save_processed_files()
            
            logger.info(f"Ingested {chunk_count} chunks from {file_path}")
            return chunk_count
            
        except Exception as e:
            logger.error(f"Error ingesting {file_path}: {e}")
            return 0
    
    async def ingest_directory(self, directory: str) -> int:
        """Recursively ingest all files in a directory"""
        total_chunks = 0
        
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if any(file.endswith(ext) for ext in self.config['file_extensions']):
                    file_path = os.path.join(root, file)
                    chunks = await self.ingest_file(file_path)
                    total_chunks += chunks
        
        return total_chunks
    
    async def query(self, question: str, k: int = None) -> Dict[str, Any]:
        """Query the knowledge base"""
        if k is None:
            k = self.config['max_results']
        
        try:
            # Embed the question
            query_embedding = await self.embed_text(question)
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
            
            return {
                'query': question,
                'results': formatted_results,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Query error: {e}")
            return {
                'query': question,
                'error': str(e),
                'results': []
            }
    
    def add_decision(self, decision: str, context: str, importance: str = "normal"):
        """Add a project decision to the knowledge base"""
        content = f"PROJECT DECISION [{importance.upper()}]:\n{decision}\n\nCONTEXT:\n{context}"
        
        # Synchronous wrapper for async embed
        loop = asyncio.new_event_loop()
        embedding = loop.run_until_complete(self.embed_text(content))
        loop.close()
        
        decision_id = f"decision_{datetime.now().timestamp()}"
        
        self.collection.add(
            ids=[decision_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[{
                'type': 'decision',
                'importance': importance,
                'timestamp': datetime.now().isoformat()
            }]
        )
        
        logger.info(f"Added decision: {decision[:50]}...")

class CodebaseWatcher(FileSystemEventHandler):
    """Watches for file changes and updates knowledge base"""
    
    def __init__(self, agent: ProjectKnowledgeAgent, config: Dict[str, Any]):
        self.agent = agent
        self.config = config
        self.update_queue = asyncio.Queue()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        if any(event.src_path.endswith(ext) for ext in self.config['file_extensions']):
            logger.info(f"File modified: {event.src_path}")
            self.loop.run_until_complete(self.agent.ingest_file(event.src_path))
    
    def on_created(self, event):
        self.on_modified(event)

class RAGServer:
    """Flask API server for RAG agent"""
    
    def __init__(self, agent: ProjectKnowledgeAgent, port: int = 5555):
        self.agent = agent
        self.app = Flask(__name__)
        CORS(self.app)
        self.port = port
        self._setup_routes()
    
    def _setup_routes(self):
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
        
        @self.app.route('/query', methods=['POST'])
        async def query():
            data = request.json
            question = data.get('question', '')
            k = data.get('k', 5)
            
            if not question:
                return jsonify({'error': 'Question required'}), 400
            
            results = await self.agent.query(question, k)
            return jsonify(results)
        
        @self.app.route('/ingest', methods=['POST'])
        async def ingest():
            data = request.json
            path = data.get('path', '')
            
            if not path or not os.path.exists(path):
                return jsonify({'error': 'Valid path required'}), 400
            
            if os.path.isfile(path):
                chunks = await self.agent.ingest_file(path)
            else:
                chunks = await self.agent.ingest_directory(path)
            
            return jsonify({'chunks_ingested': chunks})
        
        @self.app.route('/decision', methods=['POST'])
        def add_decision():
            data = request.json
            decision = data.get('decision', '')
            context = data.get('context', '')
            importance = data.get('importance', 'normal')
            
            if not decision:
                return jsonify({'error': 'Decision required'}), 400
            
            self.agent.add_decision(decision, context, importance)
            return jsonify({'status': 'Decision added'})
    
    def run(self):
        logger.info(f"Starting RAG server on port {self.port}")
        self.app.run(host='0.0.0.0', port=self.port, debug=False)

class RAGCLI:
    """Command-line interface for RAG agent"""
    
    def __init__(self, agent: ProjectKnowledgeAgent):
        self.agent = agent
    
    async def interactive_mode(self):
        """Interactive query mode"""
        print("\n🧠 RAG Knowledge Agent - Interactive Mode")
        print("Type 'exit' to quit, 'help' for commands\n")
        
        while True:
            try:
                query = input("Ask > ").strip()
                
                if query.lower() == 'exit':
                    break
                elif query.lower() == 'help':
                    self._print_help()
                elif query.lower().startswith('add decision:'):
                    decision = query[13:].strip()
                    context = input("Context > ").strip()
                    self.agent.add_decision(decision, context)
                    print("✅ Decision added to knowledge base")
                else:
                    results = await self.agent.query(query)
                    self._print_results(results)
                    
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _print_help(self):
        print("""
Commands:
  exit                     - Exit the program
  help                     - Show this help
  add decision: <text>     - Add a project decision
  <any other text>         - Query the knowledge base
        """)
    
    def _print_results(self, results: Dict[str, Any]):
        if 'error' in results:
            print(f"\n❌ Error: {results['error']}")
            return
        
        print(f"\n📊 Found {len(results['results'])} relevant results:\n")
        
        for i, result in enumerate(results['results'], 1):
            print(f"--- Result {i} ---")
            print(f"File: {result['metadata'].get('file', 'Unknown')}")
            print(f"Type: {result['metadata'].get('type', 'Unknown')}")
            
            # Truncate content for display
            content = result['content']
            if len(content) > 200:
                content = content[:200] + "..."
            print(f"Content: {content}")
            print()

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='RAG Knowledge Agent')
    parser.add_argument('command', choices=['start', 'query', 'ingest', 'watch', 'server'],
                       help='Command to run')
    parser.add_argument('--path', help='Path to ingest (for ingest command)')
    parser.add_argument('--question', help='Question to ask (for query command)')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = ProjectKnowledgeAgent(CONFIG)
    
    if args.command == 'start':
        # Start everything: watcher + server
        print("🚀 Starting RAG Knowledge Agent...")
        
        # Initial ingestion
        print("📁 Performing initial knowledge ingestion...")
        for directory in CONFIG['watch_dirs']:
            if os.path.exists(directory):
                chunks = await agent.ingest_directory(directory)
                print(f"✅ Ingested {chunks} chunks from {directory}")
        
        # Start file watcher
        observer = Observer()
        event_handler = CodebaseWatcher(agent, CONFIG)
        
        for directory in CONFIG['watch_dirs']:
            if os.path.exists(directory):
                observer.schedule(event_handler, directory, recursive=True)
                print(f"👁️  Watching {directory}")
        
        observer.start()
        
        # Start API server in background
        server = RAGServer(agent, CONFIG['api_port'])
        import threading
        server_thread = threading.Thread(target=server.run, daemon=True)
        server_thread.start()
        
        print(f"\n✅ RAG Agent running!")
        print(f"📡 API Server: http://localhost:{CONFIG['api_port']}")
        print(f"💡 Use 'rag_cli.py query' for CLI access\n")
        
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("\n👋 Shutting down...")
        
        observer.join()
    
    elif args.command == 'query':
        if args.question:
            results = await agent.query(args.question)
            cli = RAGCLI(agent)
            cli._print_results(results)
        else:
            # Interactive mode
            cli = RAGCLI(agent)
            await cli.interactive_mode()
    
    elif args.command == 'ingest':
        if not args.path:
            print("Error: --path required for ingest command")
            return
        
        if os.path.isfile(args.path):
            chunks = await agent.ingest_file(args.path)
        else:
            chunks = await agent.ingest_directory(args.path)
        
        print(f"✅ Ingested {chunks} chunks")
    
    elif args.command == 'watch':
        # Just run the watcher
        observer = Observer()
        event_handler = CodebaseWatcher(agent, CONFIG)
        
        for directory in CONFIG['watch_dirs']:
            if os.path.exists(directory):
                observer.schedule(event_handler, directory, recursive=True)
                print(f"Watching {directory}")
        
        observer.start()
        
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        
        observer.join()
    
    elif args.command == 'server':
        # Just run the API server
        server = RAGServer(agent, CONFIG['api_port'])
        server.run()

if __name__ == "__main__":
    asyncio.run(main())
