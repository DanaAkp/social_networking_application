import uuid

from sqlalchemy import column
from sqlalchemy.orm import DeclarativeBase, Query
from sqlalchemy.sql._orm_types import SynchronizeSessionArgument
from typing import Union, List

from app.reposiroty.interface import RepositoryInterface


class RepositoryPostgres(RepositoryInterface):
    def __init__(self, session):
        self.session = session

    async def get_query(self, model: DeclarativeBase) -> Query:
        return self.session.query(model)

    async def get_sort_query(self, model: DeclarativeBase, query: Query, sort_by: column,
                             order_by: str = 'asc') -> Query:
        if order_by == 'desc':
            sort_by = sort_by.desc()
        return query.order_by(sort_by)

    async def get_filter_query(self, model: DeclarativeBase, filters: List, query: Query = None) -> Query:
        if not query:
            query = await self.get_query(model)
        for f in filters:
            query = query.filter(f)
        return query

    async def delete_instance(self, instance, commit: bool = False) -> None:
        self.session.delete(instance)
        self.session.flush()
        if commit:
            self.session.commit()

    async def delete_by_query(self, query: Query, commit: bool = False,
                              synchronize_session: SynchronizeSessionArgument = "auto") -> None:
        query.delete(synchronize_session=synchronize_session)
        self.session.flush()
        if commit:
            self.session.commit()

    async def get_all_by_query(self, model: DeclarativeBase, query: Query = None) -> List:
        if not query:
            query = await self.get_query(model)
        return query.all()

    async def get_one_or_none_by_query(self, query: Query) -> DeclarativeBase:
        return query.one_or_none()

    async def get_item_by_id(
            self, model: DeclarativeBase, instance_id: Union[str, uuid.UUID, int], query: Query = None
    ) -> DeclarativeBase:
        if not query:
            query = self.session.query(model)
        return query.filter(model.id == instance_id).one_or_none()

    async def create_instance(self, model: DeclarativeBase, commit: bool = False, **kwargs) -> DeclarativeBase:
        instance = model(**kwargs)
        self.session.add(instance)
        self.session.flush()
        if commit:
            self.session.commit()
        return instance
