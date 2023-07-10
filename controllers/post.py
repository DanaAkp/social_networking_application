import datetime
import logging
import traceback

from sqlalchemy import select, insert

from models import connection
from models.post import Post


class PostService:
    async def send_post(self, text_post: str, owner_id: str):
        now = datetime.datetime.now()
        new_post = insert(Post).values(
            text_post=text_post, owner_id=owner_id,
            date_dispatch=now.date(), time_dispatch=now.time()
        )
        try:
            connection.execute(new_post)
            connection.commit()
        except Exception as error:
            connection.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise ValueError('Error with creating new post.')

    async def search_post(self, search_text: str):
        s = select(Post).where(Post.c.text_post.ilike(f'%{search_text}%'))
        result = connection.execute(s).fetchall()
        return result

    async def rate_post(self, like: bool, post_id: str, sender_id: str):
        post = connection.execute(select(Post).where(Post.c.id == post_id)).one_or_none()
        if not post:
            raise ValueError('Not found post.')
        if like:  # todo improve logic
            post.like = True
            post.dislike = False
        else:
            post.like = False
            post.dislike = True
        connection.commit()
        return post

    async def get_all_Post(self, owner_id: str):
        s = select(Post).where(Post.c.owner_id == owner_id) \
            .order_by(Post.c.date_dispatch.desc(), Post.c.time_dispatch.desc())
        result = connection.execute(s).fetchall()
        return result
