# Content Moderation System

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [System Design](#system-design)
- [Performance Considerations](#performance-considerations)
- [Conclusion](#conclusion)

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed.
- Python 3.9 or higher.

### Steps to Run the System
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd content-moderation-system
   ```
2. Build and run the Docker containers:
   ```sh
   docker-compose up --build
   ```
3. Access the API:
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) to view Swagger UI.
   
4. Monitor the system:
   - Prometheus: [http://localhost:9090](http://localhost:9090)
   - Redis: `localhost:6379`
   - PostgreSQL: `localhost:5432`

## API Documentation

### Endpoints

#### 1. Moderate Text
- **Endpoint:** `POST /api/v1/moderate/text`
- **Description:** Submits text content for moderation.
- **Request Body:**
   ```json
   {
     "text": "sample text"
   }
   ```
- **Response:**
   ```json
   {
     "task_id": "12345",
     "status": "queued"
   }
   ```

#### 2. Get Moderation Result
- **Endpoint:** `GET /api/v1/moderation/{id}`
- **Description:** Retrieves the moderation result by task ID.
- **Response:**
   ```json
   {
     "text": "sample text",
     "is_flagged": false
   }
   ```

#### 3. Get System Stats
- **Endpoint:** `GET /api/v1/stats`
- **Description:** Returns system statistics (e.g., number of requests processed).
- **Response:**
   ```json
   {
     "total_requests": 100,
     "successful_requests": 95,
     "failed_requests": 5
   }
   ```

## System Design

### Architecture
The system follows a microservices architecture with the following components:
- **Content Processing Service:** A FastAPI-based service that exposes APIs for text moderation.
- **Moderation API Integration:** Integrates with OpenAI's moderation API (or a mock server) for text analysis.
- **Queue Management:** Uses Celery with Redis for asynchronous task processing.
- **Caching:** Redis caches moderation results to reduce redundant API calls.
- **Database:** PostgreSQL stores moderation results for future reference.
- **Monitoring:** Prometheus collects metrics and monitors system health.

### Flow
1. A user submits text content via `/api/v1/moderate/text`.
2. The request is enqueued in Celery for asynchronous processing.
3. The Celery worker processes the task:
   - Checks Redis cache for existing results.
   - Calls the OpenAI moderation API (or mock) if no cached result is found.
   - Caches the result in Redis and stores it in PostgreSQL.
4. The user retrieves the moderation result via `/api/v1/moderation/{id}`.

## Performance Considerations

### Scalability
- **Asynchronous Processing:** Celery with Redis handles high throughput by processing tasks asynchronously.
- **Caching:** Redis reduces redundant API calls and improves response times.
- **Rate Limiting:** Prevents abuse and ensures fair usage of the API.

### Database Optimization
- **Indexing:** Efficient indexing on `text` and `id` columns in PostgreSQL improves query performance.
- **Connection Pooling:** SQLAlchemy's connection pooling optimizes concurrent database operations.

### Error Handling
- **Retry Mechanism:** Celery tasks implement retries with exponential backoff to handle transient failures.
- **Fallback Mechanism:** If the AI service is unavailable, the system logs the error and returns a default response.

### Monitoring
- **Prometheus:** Collects metrics such as API response times, error rates, and task processing times.
- **Health Checks:** The `/health` endpoint provides real-time system health status.

### Load Testing
- Use Locust to simulate high traffic and ensure system scalability.
- Example Locustfile:
   ```python
   from locust import HttpUser, task, between

   class ModerationUser(HttpUser):
       wait_time = between(1, 5)

       @task
       def moderate_text(self):
           self.client.post("/api/v1/moderate/text", json={"text": "sample text"})
   ```
- Run Locust:
   ```sh
   locust -f locustfile.py
   ```

## Conclusion
This system is designed to be scalable, efficient, and reliable. Leveraging FastAPI, Celery, Redis, and PostgreSQL, it efficiently moderates content while ensuring high performance. Future enhancements may include advanced monitoring (e.g., Grafana) and infrastructure scaling using Kubernetes.

