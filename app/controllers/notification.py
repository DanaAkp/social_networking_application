import logging
import traceback
from typing import List

from fastapi_socketio import SocketManager
from sqlalchemy.orm import Session

from app.models.user import Follower
from app.models.notification import Notification


class NotificationService:
    ERROR_SEND_NOTIFICATION = ''  # todo

    def __init__(self, session: Session, socket_manager: SocketManager):
        self.session = session
        self.socket_manager = socket_manager

    async def send_notification_about_new_post(self, post) -> dict:
        notifications = []
        try:
            subscribers = self.session.query(Follower).filter(Follower.subscription_id == post.owner_id).all()
            for subscriber in subscribers:
                notifications.append(Notification(
                    post_id=post.id,
                    subscriber_id=subscriber.id,
                    subscription_id=post.owner_id
                ))
            self.session.add_all(notifications)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            # todo raise Exception

        for notif in notifications:
            self.socket_manager.send(
                data=dict(
                    post_id=notif.post_id, id=notif.id, subscriber_id=notif.subscriber_id,
                    subscription_id=post.owner_id
                ),
                namespace='/notifications'
            )
        return {"success": True}

    async def get_notifications(self, user_id: str, is_read: bool = None) -> List[Notification]:
        filters = [Notification.subscriber_id == user_id]
        if is_read is not None:
            filters.append(Notification.is_read == is_read)
        return self.session.query(Notification).filter(*filters).all()
