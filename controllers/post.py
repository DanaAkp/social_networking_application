import datetime
import logging
import traceback
import uuid
from typing import List

from sqlalchemy import or_, func
from fastapi import HTTPException

from models import session
from models.post import Post, RatePosts


class PostService:
    NOT_FOUND_ERROR = 'Not found post by id {}.'
    ERROR_DELETE = 'Error with deleting post.'
    ERROR_UPDATE = 'Error with updating post.'
    ERROR_CREATE = 'Error with creating post.'
    ERROR_RATE = 'Error with rating post.'
    FORBIDDEN_RATE_POST = 'Post owner cannot rating it.'
    FORBIDDEN_DELETE_POST = 'Only post owner can delete it.'
    FORBIDDEN_UPDATE = 'Only post owner can update it.'

    async def send_post(self, body: str, owner_id: str, title) -> Post:
        new_post = Post(
            body=body, owner_id=uuid.UUID(owner_id), title=title,
            create_time=datetime.datetime.utcnow()
        )
        try:
            session.add(new_post)
            session.commit()
        except Exception as error:
            session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_CREATE)
        return new_post

    def get_query(self):
        return session.query(
            Post.id,
            Post.body,
            Post.title,
            Post.owner_id,
            Post.create_time,
            Post.modify_time,
            func.count(RatePosts.user_id).filter(RatePosts.is_like.is_(True)).label('count_likes'),
            func.count(RatePosts.user_id).filter(RatePosts.is_like.is_(False)).label('count_dislikes'),
        ).outerjoin(RatePosts, Post.id == RatePosts.post_id).group_by(Post)

    async def get_post_by_id(self, post_id: str) -> Post:
        if post := self.get_query().filter(Post.id == post_id).one_or_none():
            return post
        raise HTTPException(404, self.NOT_FOUND_ERROR.format(post_id))

    async def rate_post(self, is_like: bool, post_id: str, user_id: str) -> dict:
        if not (post := session.query(Post).filter(Post.id == post_id).one_or_none()):
            raise HTTPException(404, self.NOT_FOUND_ERROR.format(post_id))
        if post.owner_id == uuid.UUID(user_id):
            raise HTTPException(403, self.FORBIDDEN_RATE_POST)

        try:
            if rate_post_users := session.query(RatePosts).filter(RatePosts.post_id == post_id,
                                                                  RatePosts.user_id == user_id).one_or_none():
                if rate_post_users.is_like == is_like:
                    session.delete(rate_post_users)
            else:
                rate_post_users = RatePosts(post_id=post_id, user_id=user_id)
                session.add(rate_post_users)
            rate_post_users.is_like = is_like
            session.commit()
            return {'success': 'True'}
        except Exception as error:
            session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_RATE)

    async def get_all_posts(self, user_id: str, search_text: str = None) -> List[Post]:
        query = self.get_query().filter(Post.owner_id == user_id)
        if search_text:
            query = query.filter(or_(Post.body.ilike(f'%{search_text}%'), Post.title.ilike(f'%{search_text}%')))
        return query.all()

    async def edit_post(self, post_id: str, user_id: str, body, title) -> Post:
        if not (post := session.query(Post).filter(Post.id == post_id).one_or_none()):
            raise HTTPException(404, self.NOT_FOUND_ERROR)
        try:
            if post.owner_id == uuid.UUID(user_id):
                post.body = body
                post.title = title
                post.modify_time = datetime.datetime.utcnow()
                session.commit()
                return post
        except Exception as error:
            session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_UPDATE)
        raise HTTPException(403, self.FORBIDDEN_UPDATE)

    async def delete_post(self, post_id: str, owner_id: str) -> dict:
        post = session.query(Post).filter(Post.id == post_id).one_or_none()
        if not post:
            raise HTTPException(404, self.NOT_FOUND_ERROR.format(post_id))
        if post.owner_id == owner_id:
            raise HTTPException(403, self.FORBIDDEN_DELETE_POST)
        try:
            session.query(RatePosts).filter(RatePosts.post_id == post_id).delete()
            session.delete(post)
            session.commit()
            return {'success': True}
        except Exception as error:
            session.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_DELETE)
