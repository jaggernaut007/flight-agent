"""
RAG (Retrieval-Augmented Generation) service for retrieving relevant travel information.
"""
import os
import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path

class RAGService:
    """Service for retrieving relevant travel information using RAG."""
    
    def __init__(self):
        """Initialize the RAG service with data directory path."""
        self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        self.data_files = {
            'flights': os.path.join(self.data_dir, 'flights.json'),
            'hotels': os.path.join(self.data_dir, 'hotels.json'),
            'vacations': os.path.join(self.data_dir, 'vacations.json'),
        }
    
    def _load_data(self, data_type: str) -> List[Dict]:
        """
        Load data from a JSON file.
        
        Args:
            data_type: Type of data to load ('flights', 'hotels', or 'vacations')
            
        Returns:
            List of data items
        """
        if data_type not in self.data_files:
            raise ValueError(f"Invalid data type: {data_type}")
            
        try:
            with open(self.data_files[data_type], 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get(data_type, [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
    
    def search_data(self, query: str, data_type: str, max_results: int = 3) -> List[Dict]:
        """
        Search for relevant items in a specific data type.
        
        Args:
            query: Search query
            data_type: Type of data to search in ('flights', 'hotels', or 'vacations')
            max_results: Maximum number of results to return
            
        Returns:
            List of matching items
        """
        if not query or not query.strip():
            return []
            
        items = self._load_data(data_type)
        if not items:
            return []
            
        # Simple case-insensitive search in stringified item
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        matches = [item for item in items if pattern.search(json.dumps(item))]
        
        # If no matches found, return first N items as fallback
        if not matches:
            return items[:max_results]
            
        return matches[:max_results]
    
    def get_context(self, query: str, max_results: int = 2) -> Dict[str, Any]:
        """
        Retrieve relevant context from all data sources.
        
        Args:
            query: User query
            max_results: Maximum number of results per data type
            
        Returns:
            Dict containing context from different data sources
        """
        context = {}
        
        for data_type in self.data_files.keys():
            matches = self.search_data(query, data_type, max_results)
            if matches:
                context[data_type] = matches
        
        return context
    
    def format_context(self, context: Dict[str, Any]) -> str:
        """
        Format context into a readable string.
        
        Args:
            context: Context dictionary from get_context()
            
        Returns:
            Formatted context string
        """
        if not context:
            return "No relevant information found."
            
        formatted = []
        
        for data_type, items in context.items():
            if not items:
                continue
                
            formatted.append(f"=== {data_type.upper()} ===")
            
            for i, item in enumerate(items, 1):
                formatted.append(f"{i}. {json.dumps(item, indent=2, ensure_ascii=False)}")
            
            formatted.append("\n")
        
        return "\n".join(formatted).strip()
