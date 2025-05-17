from pydantic import BaseModel
import sqlite3

class NotificationRequest(BaseModel):
    user_id: str
    type: str  # email, sms, inapp
    message: str

# ✅ Define and export db connection here
db = sqlite3.connect("notifications.db", check_same_thread=False)
