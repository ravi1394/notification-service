from fastapi import APIRouter, HTTPException
from app.models import NotificationRequest, db
import json
import pika

router = APIRouter()

@router.post("/notifications")
def send_notification(notification: NotificationRequest):
    cursor = db.cursor()
    cursor.execute("INSERT INTO notifications (user_id, type, message, status) VALUES (?, ?, ?, ?)",
                   (notification.user_id, notification.type, notification.message, "queued"))
    db.commit()

    # Send to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="notifications")
    channel.basic_publish(
        exchange="",
        routing_key="notifications",
        body=notification.json()
    )
    connection.close()

    return {"status": "queued"}

@router.get("/users/{user_id}/notifications")
def get_user_notifications(user_id: str):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM notifications WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()

    return [{"id": r[0], "user_id": r[1], "type": r[2], "message": r[3], "status": r[4]} for r in rows]

@router.get("/test")
def test_route():
    return {"status": "OK"}
