
# Personal Library System

This project consists of a backend (FastAPI) and a frontend (React) service. Both services are containerized using Docker.

## Prerequisites

- Docker: Make sure Docker is installed on your machine.
- Docker Compose: Ensure Docker Compose is available to manage multi-container applications.

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/personal-library-system.git
   cd personal-library-system
   ```

2. **Build and run the services:**

   Use Docker Compose to build and start both the backend and frontend services:

   ```bash
   docker-compose up --build
   ```

   This command will:
   - Build the backend (FastAPI) service and expose it on port `8000`.
   - Build the frontend (React) service and serve it via an NGINX server on port `80`.

3. **Access the application:**

   - **Frontend**: Open your web browser and navigate to `http://localhost`. This will serve the React frontend.
   - **Backend**: You can access the FastAPI backend (e.g., the API documentation) at `http://localhost:8000/docs`.

4. **Shut down the services:**

   To stop the services, run:

   ```bash
   docker-compose down
   ```

## Project Structure

- `backend/`: Contains the FastAPI application code.
- `frontend/`: Contains the React application code.

## Networking

The project uses Docker's bridge network (`app-network`) to allow communication between the backend and frontend services.
