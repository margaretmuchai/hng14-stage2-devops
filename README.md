# hng14-stage2-devops

## Prerequisites

- Docker Engine (version 20.10 or later)
- Docker Compose (if using Docker Compose V1, or Docker Compose V2 plugin)
- Git (to clone the repository)

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hng14-stage2-devops
   ```

2. Set up environment variables:
   Create a `.env` file in the root directory (where `docker-compose.yml` is) with the following content:

   ```env
   REDIS_PASSWORD=supersecretpassword123
   ```

   Note: You can change the password if desired, but make sure it matches the one used in the API service.

3. Build and start the services:
   ```bash
   docker-compose up --build
   ```

   This will start the Redis, API, Worker, and Frontend services.

4. Verify the services are running:

   - **API**: Open http://localhost:8000/health in a web browser or use curl:
     ```bash
     curl http://localhost:8000/health
     ```
     Should return a 200 OK response.

   - **Frontend**: Open http://localhost:3000 in a web browser.
     You should see the frontend application.

   - **Worker**: The worker runs in the background. You can check its logs with:
     ```bash
     docker-compose logs worker
     ```

   - Alternatively, you can check the status of all services with:
     ```bash
     docker-compose ps
     ```

5. To stop the services, press `Ctrl+C` in the terminal where docker-compose is running, or run:
   ```bash
   docker-compose down
   ```

## Notes

- The first time you run `docker-compose up --build`, it will build the Docker images for the API, Worker, and Frontend services.
- The Redis service uses a volume to persist data between runs.

## Troubleshooting

- If you encounter issues, check the logs of the respective service:
  ```bash
  docker-compose logs <service-name>
  ```

- Ensure that ports 8000 and 3000 are not already in use on your machine.