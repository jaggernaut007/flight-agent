import os
import logging
import datetime
from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from .rag_service import RAGService
from .serpapi_flights_service import SerpApiFlightsService
from .flight_query_schema import FlightQuery

# Configure logging
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
LOG_PATH = os.path.join(LOG_DIR, 'backend.log')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class ChatService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY") 
        self.api_base = os.getenv("API_BASE") 
        self.model_name = os.getenv("MODEL_NAME")
        logger.info(f"Initializing ChatService with model: {self.model_name}, API base: {self.api_base}")
        if not self.api_key:
            logger.error("API_KEY not found in environment variables")
            raise ValueError("API_KEY not found in environment variables")
        if not self.model_name:
            logger.error("MODEL_NAME not found in environment variables")
            raise ValueError("MODEL_NAME not found in environment variables")
        # Initialize the language model
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=0.0,
            max_tokens=1000,
            openai_api_key=self.api_key,
            openai_api_base=self.api_base
        )
        logger.info("ChatOpenAI LLM initialized successfully.")
        
        # System prompt
        system_prompt = (
            "You are a helpful travel assistant. For ALL flight-related queries, you MUST ALWAYS provide both the departure and arrival airport IDs as three-letter IATA certified airport codes (not city names or ambiguous codes). "
            "If a user provides a city name, you must convert it to the correct IATA code before searching or responding. "
            "All flight dates (departure and return) must be in the future and never in the past. If the user provides a past date, ask them to provide a valid future date. "
            "Validate all flight parameters before searching. "
            "Respond with clear, concise, and accurate flight information. "
            "If you cannot find a flight, apologize and explain why. "
        )
        
        # Initialize RAG service (inactive, but not removed)
        self.rag_service = RAGService()

        # Initialize SerpApi Flights service
        self.flights_service = SerpApiFlightsService()

        # Tool for LLM: search_flights
        from langchain.tools import StructuredTool
        def search_flights_tool(departure_id: str, arrival_id: str, departure_date: str, return_date: str = None, gl: str = None, hl: str = None, currency: str = None, type: int = None):
            # City/airport code mapping for common cities
            city_to_airport = {
                # London
                "london": "LHR", "lon": "LHR", "lhr": "LHR",
                "gatwick": "LGW", "lgw": "LGW",
                "city": "LCY", "lcy": "LCY",
                # New York
                "new york": "JFK", "nyc": "JFK", "jfk": "JFK",
                "ewr": "EWR", "newark": "EWR",
                "lga": "LGA", "la guardia": "LGA",
                # Paris
                "paris": "CDG", "cdg": "CDG",
                # Los Angeles
                "los angeles": "LAX", "la": "LAX", "lax": "LAX",
                # Tokyo
                "tokyo": "HND", "hnd": "HND", "narita": "NRT", "nrt": "NRT",
                # Dubai
                "dubai": "DXB", "dxb": "DXB",
                # Mumbai
                "mumbai": "BOM", "bom": "BOM",
                # Delhi
                "delhi": "DEL", "del": "DEL",
                # Singapore
                "singapore": "SIN", "sin": "SIN",
                # Sydney
                "sydney": "SYD", "syd": "SYD",
                # Toronto
                "toronto": "YYZ", "yyz": "YYZ",
                # San Francisco
                "san francisco": "SFO", "sfo": "SFO",
                # Chicago
                "chicago": "ORD", "ord": "ORD",
                # Miami
                "miami": "MIA", "mia": "MIA",
            }

            def map_to_airport(code):
                if not code:
                    return code
                code_lower = code.strip().lower()
                mapped = city_to_airport.get(code_lower, code.upper())
                if mapped != code:
                    logger.info(f"[search_flights_tool] Mapped '{code}' to airport code '{mapped}'")
                return mapped

            departure_id_mapped = map_to_airport(departure_id)
            arrival_id_mapped = map_to_airport(arrival_id)

            # Determine type: if not provided, default to one-way (2); if return_date is present, set to round-trip (1)
            if type is None:
                type_val = 1 if return_date else 2
            else:
                type_val = type
            try:
                query = FlightQuery(
                    departure_id=departure_id_mapped,
                    arrival_id=arrival_id_mapped,
                    departure_date=departure_date,
                    return_date=return_date,
                    type=type_val,
                    gl=gl,
                    hl=hl,
                    currency=currency
                )
            except Exception as e:
                return {"error": f"Invalid flight search parameters: {e}"}
            # Only pass type if not None
            kwargs = {
                'departure_id': query.departure_id,
                'arrival_id': query.arrival_id,
                'departure_date': str(query.departure_date),
                'gl': query.gl,
                'hl': query.hl,
                'currency': query.currency
            }
            if query.return_date:
                kwargs['return_date'] = str(query.return_date)
            if query.type is not None:
                kwargs['type'] = query.type
            return self.flights_service.search_flights(**kwargs)


        self.flight_tool = StructuredTool.from_function(
            search_flights_tool,
            name="search_flights",
            description="Search for flights using departure and arrival airport codes and departure date.",
            args_schema=FlightQuery
        )

        # Create a chat prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "User: {input}\n\nToday's date: {current_date}\nUser location: {location}\nAssistant:")
        ])

        # Tool-enabled chain (OpenAI function calling)
        from langchain.agents import initialize_agent, AgentType
        self.agent = initialize_agent(
            [self.flight_tool],
            self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )
    
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
        logger.info(f"[process_message] Start processing user message: {user_message}")
        try:
            today_str = datetime.date.today().isoformat()
            if context is None:
                context = {}
            context['current_date'] = today_str
            logger.debug(f"[process_message] Context: {context}")
            location = context.get('location') if context and 'location' in context else 'unknown'
            logger.info(f"[process_message] Calling agent with prompt. Location: {location}")
            response = await self.agent.arun(
                self.prompt.format(
                    input=user_message,
                    current_date=today_str,
                    location=location
                )
            )
            logger.info(f"[process_message] LLM response: {response}")
            # Try to parse and sort flight results if present
            import json
            try:
                data = json.loads(response) if isinstance(response, str) else response
                if isinstance(data, dict) and ('best_flights' in data or 'other_flights' in data):
                    flights = []
                    for section in ['best_flights', 'other_flights']:
                        if section in data:
                            for f in data[section]:
                                # Defensive: skip if missing price or total_duration
                                price = f.get('price')
                                duration = f.get('total_duration')
                                if price is not None and duration is not None:
                                    flights.append(f)
                    # Sort by weighted optimality: price + duration (normalize duration to hours)
                    if flights:
                        # Normalize: scale price and duration
                        min_price = min(f['price'] for f in flights)
                        max_price = max(f['price'] for f in flights)
                        min_dur = min(f['total_duration'] for f in flights)
                        max_dur = max(f['total_duration'] for f in flights)
                        def score(f):
                            price_score = (f['price'] - min_price) / (max_price - min_price + 1)
                            dur_score = (f['total_duration'] - min_dur) / (max_dur - min_dur + 1)
                            return price_score + dur_score
                        flights.sort(key=score)
                        data['most_optimal_flights'] = flights[:3]  # Top 3
                        logger.info(f"[process_message] Sorted {len(flights)} flights by optimality.")
                        return json.dumps({
                            'most_optimal_flights': flights[:3],
                            'note': 'Sorted by fastest + cheapest combination',
                            'current_date': today_str
                        }, indent=2)
            except Exception as sort_e:
                logger.warning(f"[process_message] Could not sort flights: {sort_e}")
            logger.info(f"[process_message] LLM response: {response}")
            return response
        except Exception as e:
            error_msg = f"Error in process_message: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return "I'm sorry, I encountered an error while processing your request. Please try again later."

# Singleton instance
chat_service = ChatService()
