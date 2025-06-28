# Django Internship Assignment

## Overview
This project demonstrates backend skills using Django, Django REST Framework, JWT authentication, Celery with Redis, and Telegram bot integration.

## Features
- User registration and login (JWT, with DRF serializer validation)
- Public and protected API endpoints
- Celery background task: send welcome email after registration (with retries and template)
- Telegram bot: collects and stores Telegram usernames (with error handling)
- Swagger/OpenAPI documentation
- CORS enabled for API
- Sample unit tests for registration

## Requirements
- Python 3.8+
- Redis server
- (Optional) Docker for Redis

## Setup Instructions

1. **Clone the repository**
   ```
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   DJANGO_SECRET_KEY=your-secret-key
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_email_password_or_app_password
   EMAIL_USE_TLS=True
   EMAIL_USE_SSL=False
   DEFAULT_FROM_EMAIL=your_email@gmail.com
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```

4. **Apply migrations**
   ```
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```
   python manage.py createsuperuser
   ```

6. **Run Redis**
   - With Docker:
     ```
     docker run -p 6379:6379 redis
     ```
   - Or run `redis-server.exe` if on Windows.

7. **Start Django server**
   ```
   python manage.py runserver
   ```

8. **Start Celery worker**
   ```
   celery -A backend worker --loglevel=info
   ```

9. **Run the Telegram bot**
   ```
   python api/telegram_bot.py
   ```

10. **Run tests**
    ```
    python manage.py test tests/
    ```

## API Documentation

### Swagger/OpenAPI
- Visit `/swagger/` for interactive API docs.
- Visit `/redoc/` for Redoc documentation.

### Registration
- **POST** `/api/register/`
  - Body: `{ "username": "user", "password": "pass", "email": "email" }`
  - Registers a new user and sends a welcome email (background task with retries and template).
  - Uses DRF serializer for validation and error messages.

### Obtain JWT Token
- **POST** `/api/token/`
  - Body: `{ "username": "user", "password": "pass" }`
  - Returns access and refresh tokens.

### Refresh JWT Token
- **POST** `/api/token/refresh/`
  - Body: `{ "refresh": "<refresh_token>" }`

### Public Endpoint
- **GET** `/api/public/`
  - No authentication required.

### Protected Endpoint
- **GET** `/api/protected/`
  - Requires JWT authentication (add `Authorization: Bearer <access_token>` header).

## Telegram Bot
- Start a chat with your bot and send `/start`.
- Your Telegram username will be saved in the database.
- Bot includes error handling for network and database issues.

## Static and Media Files
- For development, static files are served automatically.
- For production, collect static files:
  ```
  python manage.py collectstatic
  ```
- Configure a web server (e.g., Nginx) to serve static and media files in production.

## Deployment Options
- You can deploy this project to platforms like Heroku, Render, or use Docker for containerized deployment.
- For Docker, create a `Dockerfile` and use environment variables as shown above.

## Notes
- All secrets and credentials should be kept in the `.env` file (never commit this file).
- For production, set `DJANGO_DEBUG=False` and use strong secrets.
- CORS is enabled for all origins (for demo); restrict in production.
- See `tests/` for sample unit tests for registration.

---

**Good luck!** 