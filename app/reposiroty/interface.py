import uuid
from abc import abstractmethod, ABCMeta
from typing import Union, List

from sqlalchemy import column
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm.query import Query
from sqlalchemy.sql._orm_types import SynchronizeSessionArgument


class RepositoryInterface(object):
    __metaclass__ = ABCMeta

    def __int__(self, session: Session):
        self.session = session

    @abstractmethod
    async def create_instance(self, model: DeclarativeBase, commit: bool = False, **kwargs) -> DeclarativeBase:
        pass

    @abstractmethod
    async def delete_instance(self, instance, commit: bool = False) -> None:
        pass

    @abstractmethod
    async def delete_by_query(self, query: Query, commit: bool = False,
                              synchronize_session: SynchronizeSessionArgument = "auto") -> None:
        pass

    @abstractmethod
    async def get_item_by_id(
            self, model: DeclarativeBase, instance_id: Union[str, uuid.UUID, int], query: Query = None
    ) -> DeclarativeBase:
        pass

    @abstractmethod
    async def get_query(self, model: DeclarativeBase) -> Query:
        pass

    @abstractmethod
    async def get_filter_query(self, model: DeclarativeBase, filters: list, query: Query = None) -> Query:
        pass

    @abstractmethod
    async def get_sort_query(self, model: DeclarativeBase, query: Query, sort_by: column, order_by: str) -> Query:
        pass

    @abstractmethod
    async def get_all_by_query(self, model: DeclarativeBase, query: Query = None) -> List:
        pass

    @abstractmethod
    async def get_one_or_none_by_query(self, query: Query) -> DeclarativeBase:
        pass

    @abstractmethod
    async def rollback(self):
        self.session.rollback()

    @abstractmethod
    async def commit(self):
        self.session.commit()
