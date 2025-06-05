import os
import logging
from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from .rag_service import RAGService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class ChatService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("DEEPSEEK_API_URL") or os.getenv("OPENAI_API_URL")
        if not self.api_key:
            raise ValueError("Neither DEEPSEEK_API_KEY nor OPENAI_API_KEY found in environment variables")
        
        # Initialize the language model
        # Change model name as per requirements. DeepSeek uses deepseek-chat, OpenAI uses gpt-3.5-turbo
        self.llm = ChatOpenAI(
            model_name="deepseek-chat",
            temperature=0.7,
            max_tokens=1000,
            openai_api_key=self.api_key,
            openai_api_base=self.api_base
        )
        
        # System prompt
        system_prompt = """You are a helpful travel assistant. You can help users with travel related queries.and information about flights, vacations and hotel bookings.
        If there are multiple options, provide all of them. Ensure to provide information from the database only. If there are no flights, vacations or hotel bookings available, provide a message to the user.
        Be friendly, concise, and provide helpful information.
        """
        
        # Initialize RAG service
        self.rag_service = RAGService()
        
        # Create a chat prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Context: {context}\n\nUser: {input}\n\nAssistant:")
        ])
        
        # Create a chain
        self.chain = self.prompt | self.llm
    
    def _get_rag_context(self, user_message: str) -> str:
        """
        Get relevant context using the RAG service.
        
        Args:
            user_message: The user's message to get context for
            
        Returns:
            Formatted context string
        """
        if not user_message or not user_message.strip():
            return "No context available."
            
        try:
            # Get RAG context
            context = self.rag_service.get_context(user_message)
            # Format the context into a readable string
            return self.rag_service.format_context(context)
        except Exception as e:
            logger.warning(f"Error retrieving RAG context: {e}")
            return "Error retrieving travel information. Please try again later."
            

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
            # Get relevant context (flights, hotels, etc.)
            other_context = self._rag_retrieve_context(user_message)
            
            # Build the context string for the LLM
            context_parts = []
            
            # Add other context (flights, hotels, vacations)
            for key, items in other_context.items():
                if items:
                    context_parts.append(f"{key.upper()}:\n" + "\n".join(items))
            
            # Add any existing context from the conversation
            if context:
                context_parts.append("CONVERSATION CONTEXT:" + 
                                  "\n".join(f"- {k}: {v}" for k, v in context.items() if v))
            
            # Combine all context parts
            context_str = "\n\n".join(part for part in context_parts if part)
            
            # Log the context for debugging
            logger.debug(f"Context for LLM:\n{context_str}")
            
            # If we're in a conversation flow, maintain context
            conversation_context = dict(context or {})
            if 'conversation' not in conversation_context:
                conversation_context['conversation'] = []
            
            # Add user message to conversation history (last 3 messages)
            conversation_context['conversation'].append(f"User: {user_message}")
            conversation_context['conversation'] = conversation_context['conversation'][-3:]  # Keep last 3 messages
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
