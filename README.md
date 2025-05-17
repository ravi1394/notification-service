# Notification Service

## Features
- Send notifications (email, sms, in-app)
- Queue-based async delivery (RabbitMQ)
- Retry on failure
- REST API via FastAPI

## Setup

```bash
git clone ...
cd notification-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
