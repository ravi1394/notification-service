import pika
import json
from time import sleep
from app.models import db
from app.services import email, sms, inapp

def process(notification):
    msg = notification["message"]
    n_type = notification["type"]

    if n_type == "email":
        return email.send_email(msg)
    elif n_type == "sms":
        return sms.send_sms(msg)
    elif n_type == "inapp":
        return inapp.send_inapp(msg)
    return False

def update_status(user_id, message, status):
    cursor = db.cursor()
    cursor.execute("UPDATE notifications SET status = ? WHERE user_id = ? AND message = ?",
                   (status, user_id, message))
    db.commit()

def callback(ch, method, properties, body):
    notification = json.loads(body)
    print(f"Received: {notification}")
    retry_count = 0

    while retry_count < 3:
        success = process(notification)
        if success:
            update_status(notification["user_id"], notification["message"], "delivered")
            print("Delivered ✅")
            break
        retry_count += 1
        print(f"Retrying ({retry_count})...")
        sleep(2)

    if retry_count == 3:
        update_status(notification["user_id"], notification["message"], "failed")
        print("Failed ❌")

# ✅ RabbitMQ listener
def main():
    print("Worker started. Waiting for messages...")
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="notifications")
    channel.basic_consume(queue="notifications", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()
