from dbconfig import Database
from datetime import datetime
import pytz

class MessageModel:
    def __init__(self, message: str, image_url: str):
        self.message = message
        self.image_url = image_url

    async def save(self):
        query = """
            INSERT INTO `messages` (message, image_url, created_at)
            VALUES (%s, %s, %s)
        """
        params = (self.message, self.image_url, datetime.utcnow())
        Database.execute_query(query, params)

    @staticmethod
    async def get_messages():
        query = "SELECT * FROM messages ORDER BY created_at DESC"
        messages = Database.execute_query(query, dictionary=True)
        
        taipei_tz = pytz.timezone("Asia/Taipei")
        
        for message in messages:
            utc_time = message.get("created_at")
            if utc_time:
                if utc_time.tzinfo is None:
                    utc_time = pytz.utc.localize(utc_time)
                taipei_time = utc_time.astimezone(taipei_tz)
                message["created_at"] = taipei_time.isoformat()
            message["image"] = message.pop("image_url")
        return messages
    
    @staticmethod
    async def delete_message(message_id: int):
        query = "DELETE FROM messages WHERE id = %s"
        try:
            Database.execute_query(query, (message_id,))
            return {"ok": True}
        except Exception as e:
            print(e)
            return {"error": True}