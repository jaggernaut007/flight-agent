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

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
   
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the project root directory:
   ```bash
   cd ..
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

## Running the Application

### Development Mode

1. **Start the backend server**:
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```

2. **Start the frontend development server**:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173`

## Docker Setup & Deployment

This project includes Docker configuration for easy deployment and development. You can run the entire application stack using Docker Compose.

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

### Building for Production

This project includes a production-ready Docker setup with optimized configurations for both frontend and backend services.

#### Production Stack Overview

- **Frontend**: Served via Nginx with gzip compression and caching
- **Backend**: Python 3.11 with Uvicorn
- **Networking**: Dedicated bridge network for secure inter-service communication
- **Optimizations**: Multi-stage builds, proper layer caching, and security headers

#### Production Files

- `docker-compose.prod.yml` - Production Docker Compose configuration
- `Dockerfile.frontend.prod` - Optimized frontend Dockerfile
- `backend/Dockerfile.prod` - Optimized backend Dockerfile
- `nginx.conf` - Nginx configuration with security headers and caching

#### Building and Running

1. **Build the production images**:
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Start the production stack**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Verify the services are running**:
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   ```

#### Accessing the Application

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

#### Production Features

- **Performance**:
  - Gzip compression for all responses
  - Static file caching with proper cache headers
  - Optimized Nginx configuration

- **Security**:
  - Security headers (CSP, XSS Protection, etc.)
  - Minimal base images
  - Non-root user execution
  - Health checks for both services

- **Reliability**:
  - Automatic restarts on failure
  - Resource constraints
  - Dedicated network for service communication

#### Monitoring and Maintenance

- **View logs**:
  ```bash
  # All services
  docker-compose -f docker-compose.prod.yml logs -f
  
  # Specific service
  docker-compose -f docker-compose.prod.yml logs -f frontend
  docker-compose -f docker-compose.prod.yml logs -f backend
  ```

- **Stop the services**:
  ```bash
  docker-compose -f docker-compose.prod.yml down
  ```

- **Update the services**:
  ```bash
  docker-compose -f docker-compose.prod.yml pull
  docker-compose -f docker-compose.prod.yml up -d --build
  ```

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
