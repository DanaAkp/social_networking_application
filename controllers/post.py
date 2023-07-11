import datetime
import logging
import traceback
from typing import List

from sqlalchemy import or_
from fastapi import HTTPException

from models import session
from models.post import Post, posts_users


class PostService:
    NOT_FOUND_ERROR = 'Not found post by id {}.'
    ERROR_DELETE = 'Error with deleting post.'
    ERROR_UPDATE = 'Error with updating post.'
    ERROR_CREATE = 'Error with creating post.'
    FORBIDDEN_RATE_POST = 'Post owner cannot rating it.'
    FORBIDDEN_DELETE_POST = 'Only post owner can delete it.'

    async def send_post(self, text_post: str, owner_id: str, title) -> Post:
        new_post = Post(
            body=text_post, owner_id=owner_id, title=title,
            create_time=datetime.datetime.now()
        )
        try:
            session.add(new_post)
            session.commit()
        except Exception as error:
            session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_CREATE)
        return new_post

    async def search_post(self, search_text: str) -> List[Post]:
        s = session.query(Post).filter(
            or_(Post.body.ilike(f'%{search_text}%'), Post.title.ilike(f'%{search_text}%'))
        )
        return s.all()

    async def rate_post(self, like: bool, dislike: bool, post_id: str, user_id: str) -> Post:
        if post := session.query(posts_users).filter(posts_users.post_id == post_id,
                                                     posts_users.user_id == user_id).one_or_none():
            if post.post.owner_id == user_id:
                raise HTTPException(403, self.FORBIDDEN_RATE_POST)
        else:
            post = Post(post_id=post_id, user_id=user_id)
        post.like = like
        post.dislike = dislike
        session.add(post)
        session.commit()
        return post

    async def get_all_posts(self, user_id: str) -> List[Post]:
        return session.query(Post).filter(Post.owner_id == user_id).all()

    async def edit_post(self, post_id: str, body, title) -> Post:
        update_post = session.query(Post).filter(Post.id == post_id)
        try:
            if result := update_post.one_or_none():
                result.body = body
                result.title = title
                result.modify_time = datetime.datetime.now()
                session.commit()
                return result
        except Exception as error:
            session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_UPDATE)
        raise HTTPException(404, self.NOT_FOUND_ERROR)

    async def delete_post(self, post_id: str, owner_id: str) -> dict:
        post = session.query(Post).filter(Post.id == post_id).one_or_none()
        if not post:
            raise HTTPException(404, self.NOT_FOUND_ERROR.format(post_id))
        if post.owner_id == owner_id:
            raise HTTPException(403, self.FORBIDDEN_DELETE_POST)
        try:
            session.delete(post)
            session.commit()
            return {'success': True}
        except Exception as error:
            session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_DELETE)
