import os
import logging
from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

import json
import re

class ChatService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Neither DEEPSEEK_API_KEY nor OPENAI_API_KEY found in environment variables")
        
        # Initialize the language model
        self.llm = ChatOpenAI(
            model_name="deepseek-chat",
            temperature=0.7,
            max_tokens=1000,
            openai_api_key=self.api_key,
            openai_api_base="https://api.deepseek.com/v1"
        )
        
        # System prompt
        system_prompt = """You are a helpful travel assistant. You can help users find flights, 
        hotels, and vacation packages. Be friendly and provide accurate information.
        """
        
        # Create a chat prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Context: {context}\n\nUser: {input}\n\nAssistant:")
        ])
        
        # Create a chain
        self.chain = self.prompt | self.llm
    
    def _rag_retrieve_context(self, user_message: str, max_results: int = 2) -> Dict[str, Any]:
        """
        Retrieve relevant context from flights, hotels, and vacations data based on the user query.
        Returns a dict with context summaries for each data type.
        """
        data_dir = os.path.join(os.path.dirname(__file__), '../data')
        files = {
            'flights': os.path.join(data_dir, 'flights.json'),
            'hotels': os.path.join(data_dir, 'hotels.json'),
            'vacations': os.path.join(data_dir, 'vacations.json'),
        }
        context = {}
        pattern = re.compile(re.escape(user_message), re.IGNORECASE)
        
        for key, path in files.items():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                items = data.get(key, [])
                # Simple keyword search in stringified item
                matches = [item for item in items if pattern.search(json.dumps(item))]
                # If not enough matches, try a fallback: show first N
                if not matches:
                    matches = items[:max_results]
                else:
                    matches = matches[:max_results]
                # Summarize matches
                summaries = []
                for item in matches:
                    if key == 'flights':
                        summaries.append(f"Flight {item.get('flightNumber', '')} from {item.get('departure', {}).get('city', '')} to {item.get('arrival', {}).get('city', '')} on {item.get('departure', {}).get('date', '')}, Status: {item.get('status', '')}, Price (economy): {item.get('price', {}).get('economy', '')}")
                    elif key == 'hotels':
                        summaries.append(f"Hotel {item.get('name', '')} in {item.get('address', {}).get('city', '')}, {item.get('starRating', '')} stars, Price: {item.get('priceRange', {}).get('low', '')}-{item.get('priceRange', {}).get('high', '')} {item.get('priceRange', {}).get('currency', '')}")
                    elif key == 'vacations':
                        summaries.append(f"Vacation {item.get('name', '')} in {item.get('destination', {}).get('city', '')}, {item.get('duration', {}).get('days', '')} days / {item.get('duration', {}).get('nights', '')} nights, Highlights: {', '.join(item.get('highlights', [])[:2]) if 'highlights' in item else ''}")
                context[key] = summaries
            except Exception as e:
                logger.warning(f"Failed to retrieve context for {key}: {e}")
                context[key] = []
        return context

    async def process_message(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process a user message and return the assistant's response.
        
        Args:
            user_message: The message from the user
            context: Optional context dictionary for the conversation
        Returns:
            str: The assistant's response
        """
        try:
            # RAG context retrieval
            rag_context = self._rag_retrieve_context(user_message)
            # Merge with any external context
            merged_context = dict(context or {})
            for k, v in rag_context.items():
                if v:
                    merged_context[k] = '\n'.join(v)
            context_str = "\n".join([f"{k}: {v}" for k, v in merged_context.items()])
            # Get the response from the language model
            response = await self.chain.ainvoke({
                "context": context_str,
                "input": user_message
            })
            # Extract the content from the AIMessage object
            if hasattr(response, 'content'):
                return response.content.strip()
            return str(response).strip()
        except Exception as e:
            error_msg = f"Error in process_message: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return "I'm sorry, I encountered an error while processing your request. Please try again later."

# Singleton instance
chat_service = ChatService()
