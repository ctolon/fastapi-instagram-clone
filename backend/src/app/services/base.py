
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
import abc

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from app.db.base_class import Base
from app.repo.base import GenericCrudRepository

ModelType = TypeVar("ModelType", bound=Base)
RepoType = TypeVar("RepoType", bound=GenericCrudRepository)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

    
class GenericCrudService(abc.ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType, RepoType], metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def __init__(self, repo: RepoType):
        """
        Generic Crud Service with default methods to Create, Read, Update, Delete as async (CRUD).

        **Parameters**

        * `repo`: A Repository class which inherits from GenericCrudRepository
        * `schema`: A Pydantic model (schema) class
        """
        self.repo = repo
        
    
    async def get(self, db: AsyncSession, id: int) -> ModelType:
        result = await self.repo.get(id=id, db=db)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repo.model.__name__} with id {id} not found",
            )
        return result
    
    async def get_all(self,db: AsyncSession, skip: int=0, limit: int = 100) -> List[ModelType]:
        result = await self.repo.get_all(db=db, skip=skip, limit=limit)
        return result
    
    async def update(self, db: AsyncSession, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        model = await self.repo.get(db=db, id=id)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repo.model.__name__} with id {id} not found",
            )
        result = await self.repo.update(db=db, id=id, obj_in=obj_in)
        return result
    
    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        result = await self.repo.create(db=db, obj_in=obj_in)
        return result

    async def remove(self, db: AsyncSession, id: int) -> ModelType:
        model = await self.repo.get(db=db, id=id)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repo.model.__name__} with id {id} not found",
            )
        result = await self.repo.remove(db=db, id=id)
        return result

