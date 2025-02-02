from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
import abc

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

    
class GenericCrudRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], metaclass=abc.ABCMeta):
    """Generic CRUD repository Implementation as Base Repository."""
    
    @abc.abstractmethod
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete as async (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        
    async def get(
        self,
        db: AsyncSession,
        id: Any
        ) -> Optional[ModelType]:
        """Get a single object by ID operation."""
        
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        *,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
        ) -> List[ModelType]:
        """Get multiple objects with optional `skip` and `limit` parameters operation."""
        
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(
        self,
        *, db: AsyncSession,
        obj_in: CreateSchemaType
        ) -> ModelType:
        """"Create an object operation."""
        
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        *,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an object operation."""
        
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        *,
        db: AsyncSession,
        id: int
        ) -> ModelType:
        """Remove an object operation."""
        
        obj = await db.get(self.model, id)
        await db.delete(obj)
        await db.commit()
        return obj
