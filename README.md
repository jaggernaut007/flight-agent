# Flight Assistance Application

A comprehensive flight assistance application that helps users find and book flights, hotels, and vacation packages with AI-powered chat support.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Structure](#database-structure)
- [Best Practices for Prompting](#best-practices-for-prompting)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- AI-powered flight search and booking
- Hotel and vacation package recommendations
- Interactive chat interface
- Real-time flight status updates
- User authentication and profile management
- Responsive design for all devices

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- npm or yarn
- Git

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Alternative) You can use [uv](https://github.com/astral-sh/uv) for faster dependency management and running the backend:
   ```bash
   # Install uv if not already installed
   pip install uv
   # Install dependencies (using pyproject.toml)
   uv pip install .
   # Run the backend (hot reload)
   uvicorn main:app --reload
   # Or, using uv's built-in runner (if available):
   uv run main:app --reload
   ```

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd ../frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

## Running the Application

### Development Mode

1. **Start the backend server** (choose one):
   ```bash
   # Using uvicorn (default)
   cd backend
   uvicorn main:app --reload
   # Or using Python module
   python -m uvicorn main:app --reload
   # Or using uv (if installed)
   uv run main:app --reload
   ```

2. **Start the frontend development server**:
   ```bash
   cd ../frontend
   npm run dev
   # or
   yarn dev
   ```

3. Open your browser and navigate to `http://localhost:5173`

## Docker Development Setup

This project includes Docker configuration for local development. You can run the entire application stack using Docker Compose.

### Prerequisites

- Docker Engine (v20.10+)
- Docker Compose (v2.0+)

### Quick Start

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd flight-assistance
   ```

2. **Set up environment variables**:
   - Copy `.env.example` to `.env` in both root and backend directories
   - Update the variables with your configuration

3. **Build and start the containers**:
   ```bash
   docker-compose up --build
   ```
   
   This will:
   - Build the frontend and backend images
   - Start both services
   - Make the application available at `http://localhost:4173`

### Available Services

- **Frontend**: `http://localhost:4173`
- **Backend API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`

### Managing the Services

- **Start services in detached mode**:
  ```bash
  docker-compose up -d
  ```

- **View logs**:
  ```bash
  # All services
  docker-compose logs -f
  
  # Specific service
  docker-compose logs -f frontend
  docker-compose logs -f backend
  ```

- **Stop services**:
  ```bash
  docker-compose down
  ```

## Environment Setup

### Setting Up Environment Variables

1. Copy the example environment file and fill in your API keys:
   ```bash
   cd backend
   cp .env.example .env
   # Then edit .env and provide your API keys
   ```

2. The `.env.example` file includes the following keys:
   ```env
   # DeepSeek API configuration
   # API_KEY=your-deepseek-api-key
   # API_BASE=https://api.deepseek.com/v1/

   # OpenAI API configuration
   API_KEY=your-openai-api-key
   API_BASE=https://api.openai.com/v1/
   MODEL_NAME=gpt-4o

   # OpenWeather API configuration
   OPENWEATHER_API_KEY=your-openweather-api-key

   # SERPAPI configuration
   SERPAPI_KEY=your-SERPAPI-api-key
   ```
   - Un-comment and fill in the DeepSeek section if you use DeepSeek.
   - Fill in your OpenAI, OpenWeather, and SERPAPI keys as needed.

3. **Security:**
   - Ensure `.env` is listed in `.gitignore` to avoid committing secrets.

## Deployment

### Pushing to Docker Hub

To push the images to Docker Hub:

1. **Login to Docker Hub**:
   ```bash
   docker login
   ```

2. **Tag and push the backend image**:
   ```bash
   docker tag flight-assistance-backend:latest yourusername/flight-assistant-backend:latest
   docker push yourusername/flight-assistant-backend:latest
   ```

3. **Tag and push the frontend image**:
   ```bash
   docker tag flight-assistance-frontend:latest yourusername/flight-assistant-frontend:latest
   docker push yourusername/flight-assistant-frontend:latest
   ```

### Environment Variables

#### Backend
- `PORT`: Port to run the backend server (default: 8000)
- `ENVIRONMENT`: Runtime environment (development/production)
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for authentication

#### Frontend
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

### Troubleshooting

- **Port conflicts**: Ensure ports 8000 and 4173 are available or update them in `docker-compose.yml`
- **Build failures**: Check the logs with `docker-compose logs -f`
- **Environment variables**: Verify all required variables are set in `.env` files

For production deployments, consider using a reverse proxy like Nginx and setting up SSL certificates with Let's Encrypt.

### Start the Backend Server

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\Activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   You should see `(venv)` appear at the start of your command prompt when activated.

3. Install the required dependencies (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The server will start on `http://localhost:8000`
   - The `--reload` flag enables auto-reload for development
   - Access API documentation at `http://localhost:8000/docs`

### Start the Frontend Development Server

1. In a new terminal, navigate to the project root:
   ```bash
   cd path/to/flight-assistance
   ```

2. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   The application will be available at `http://localhost:3000`

## API Documentation

Once the backend server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Available Endpoints

#### Health Check
- `GET /api/health` - Check if the API is running
  - **Response**:
    ```json
    {
      "status": "ok",
      "message": "Travel Assistant API is running"
    }
    ```

#### Chat Endpoint
- `POST /api/chat` - Chat with the AI travel assistant
  - **Request Body**:
    ```json
    {
      "message": "Find me a flight from London to Paris",
      "context": {}
    }
    ```
  - **Response**:
    ```json
    {
      "response": "Here are some flights from London to Paris...",
      "context": {}
    }
    ```

The chat endpoint is the primary interface for interacting with the travel assistant. It handles natural language queries about flights, hotels, and vacation packages.

## Database Structure

The application uses JSON files for data storage. The data is stored in the `backend/data/` directory:

### Flights (`flights.json`)
```json
{
  "flights": [
    {
      "id": "string",
      "airline": "string",
      "flight_number": "string",
      "origin": "string",
      "destination": "string",
      "departure_time": "datetime",
      "arrival_time": "datetime",
      "price": number,
      "seats_available": number
    }
  ]
}
```

### Hotels (`hotels.json`)
```json
{
  "hotels": [
    {
      "id": "string",
      "name": "string",
      "location": "string",
      "price_per_night": number,
      "rating": number,
      "amenities": ["string"],
      "available_rooms": number
    }
  ]
}
```

### Vacations (`vacations.json`)
```json
{
  "vacations": [
    {
      "id": "string",
      "name": "string",
      "destination": "string",
      "duration_days": number,
      "price": number,
      "included": ["string"],
      "hotel_id": "string"
    }
  ]
}
```

## Best Practices for Prompting

To get the best results from the AI assistant, follow these guidelines:

1. **Be Specific**: Include relevant details like:
   - Travel dates
   - Number of travelers
   - Preferred airlines or hotels
   - Budget constraints
   - Special requirements (e.g., wheelchair access, dietary restrictions)

2. **Example Prompts**:
   - "Find me a round-trip flight from New York to London for 2 adults from June 15-30, 2023"
   - "Show me 4-star hotels in Paris with a pool and gym"
   - "Suggest a 7-day vacation package to Japan for a family of 4 in December"

3. **Refine Your Search**:
   - Use filters to narrow down results
   - Sort by price, duration, or rating
   - Ask for recommendations based on your preferences

## Troubleshooting

### Common Issues

1. **Backend Server Not Starting**
   - Ensure all dependencies are installed
   - Check if port 8000 is available
   - Verify Python virtual environment is activated

2. **Frontend Not Connecting to Backend**
   - Ensure the backend server is running
   - Check CORS settings in the backend
   - Verify API endpoints in frontend configuration

3. **Missing Dependencies**
   - Run `npm install` or `yarn` in the frontend directory
   - Run `pip install -r requirements.txt` in the backend directory

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 License - see the [LICENSE](LICENSE) file for details.
