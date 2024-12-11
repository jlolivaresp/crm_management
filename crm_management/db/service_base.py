from typing import TypeVar, Generic, List, Optional, Any, Type

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from crm_management.db.orm_base import Base

T = TypeVar("T", bound=Base)


class DBBaseAPI(Generic[T]):
    """Abstract base class for db CRUD operations."""

    def __init__(self, session: Session, model: T):
        self.session = session
        self.model = model

    def create(self, instance: T) -> T:
        """Create and persist a new instance."""
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def get(self, id: int) -> Optional[T]:
        """Retrieve an instance by its primary key."""
        try:
            return self.session.query(self.model).filter_by(id=id).one()
        except NoResultFound:
            return None

    def get_field_and_value(self, field: str, value: Any) -> List[T]:
        """Retrieve all instances where a given field matches a value."""
        if not hasattr(self.model, field):
            raise AttributeError(f"{self.model.__name__} has no attribute '{field}'")
        return (
            self.session.query(self.model)
            .filter(getattr(self.model, field) == value)
            .all()
        )

    def find_by_fields(self, **fields) -> T | None:
        """Find a single record by a combination of fields."""
        return (
            self.session.query(self.model)
            .filter(
                and_(
                    *(
                        getattr(self.model, key) == value
                        for key, value in fields.items()
                    )
                )
            )
            .one_or_none()
        )

    def get_all(self) -> List[T]:
        """Retrieve all instances."""
        return self.session.query(self.model).all()

    def update(self, id: int, updates: Type[T]) -> Optional[T]:
        """Update an existing instance by its primary key."""
        instance = self.get(id)
        if instance:
            for key, value in vars(updates).items():
                if key.startswith("_"):  # Skip SQLAlchemy internal attributes
                    continue
                setattr(instance, key, value)
            self.session.commit()
            self.session.refresh(instance)
            return instance
        return None

    def delete(self, id: int) -> bool:
        """Delete an instance by its primary key."""
        instance = self.get(id)
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        return False
