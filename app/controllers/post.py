import datetime
import logging
import traceback
import uuid
from typing import List

from sqlalchemy import or_, func
from fastapi import HTTPException

from app.models import repo
from app.models.post import Post, RatePosts

repo.get_post_query = lambda: repo.session.query(
    Post.id.label('id'),
    Post.body.label('body'),
    Post.title.label('title'),
    Post.owner_id.label('owner_id'),
    Post.create_time.label('create_time'),
    Post.modify_time.label('modify_time'),
    func.count(RatePosts.user_id).filter(RatePosts.is_like.is_(True)).label('count_likes'),
    func.count(RatePosts.user_id).filter(RatePosts.is_like.is_(False)).label('count_dislikes'),
).select_from(Post).outerjoin(RatePosts, Post.id == RatePosts.post_id).group_by(Post)


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

        try:
            new_post = await repo.create_instance(
                model=Post,
                commit=True,
                body=body, owner_id=uuid.UUID(owner_id), title=title,
                create_time=datetime.datetime.utcnow()
            )
        except Exception as error:
            await repo.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_CREATE)
        return new_post

    async def get_post_by_id(self, post_id: str) -> Post:
        if post := await repo.get_item_by_id(Post, post_id, repo.get_post_query()):
            return post
        raise HTTPException(404, self.NOT_FOUND_ERROR.format(post_id))

    async def rate_post(self, is_like: bool, post_id: str, user_id: str) -> dict:
        if not (post := await repo.get_item_by_id(Post, post_id)):
            raise HTTPException(404, self.NOT_FOUND_ERROR.format(post_id))
        if post.owner_id == uuid.UUID(user_id):
            raise HTTPException(403, self.FORBIDDEN_RATE_POST)

        try:
            query = await repo.get_filter_query(RatePosts, (RatePosts.post_id == post_id,
                                                            RatePosts.user_id == user_id))
            if rate_post_users := await repo.get_one_or_none_by_query(query):
                if rate_post_users.is_like == is_like:
                    await repo.delete_instance(rate_post_users)
            else:
                rate_post_users = await repo.create_instance(RatePosts, commit=False, post_id=post_id, user_id=user_id)
            rate_post_users.is_like = is_like
            await repo.commit()
            return {'success': 'True'}
        except Exception as error:
            await repo.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_RATE)

    async def get_all_posts(self, user_id: str, search_text: str = None) -> List[Post]:
        query = await repo.get_filter_query(Post, (Post.owner_id == user_id,), repo.get_post_query())
        if search_text:
            query = await repo.get_filter_query(
                Post,
                (or_(Post.body.ilike(f'%{search_text}%'), Post.title.ilike(f'%{search_text}%')),)
            )
        return await repo.get_all_by_query(Post, query)

    async def edit_post(self, post_id: str, user_id: str, body, title) -> Post:
        if not (post := await repo.get_item_by_id(Post, post_id), repo.get_post_query()):
            raise HTTPException(404, self.NOT_FOUND_ERROR)
        try:
            if post.owner_id == uuid.UUID(user_id):
                post.body = body
                post.title = title
                post.modify_time = datetime.datetime.utcnow()
                await repo.commit()
                return post
        except Exception as error:
            await repo.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_UPDATE)
        raise HTTPException(403, self.FORBIDDEN_UPDATE)

    async def delete_post(self, post_id: str, owner_id: str) -> dict:
        post = await repo.get_item_by_id(Post, post_id)
        if not post:
            raise HTTPException(404, self.NOT_FOUND_ERROR.format(post_id))
        if post.owner_id == owner_id:
            raise HTTPException(403, self.FORBIDDEN_DELETE_POST)
        try:
            query = await repo.get_filter_query(RatePosts, (RatePosts.post_id == post_id,))
            await repo.delete_by_query(query)
            await repo.delete_instance(post)
        except Exception as error:
            await repo.rollback()
            logging.error(f'Error: {error}, traceback: {traceback.format_exc()}')
            raise HTTPException(400, self.ERROR_DELETE)
        await repo.commit()
        return {'success': True}
