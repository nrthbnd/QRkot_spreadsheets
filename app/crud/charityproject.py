from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from constants import (
    COLLECTION_TIME_FORMAT, WAS_FULLY_INVESTED,
    NAME_LABEL, DESCRIPTION_LABEL, COLLECTION_TIME_LABEL,
)
from app.crud.base import CRUDBase
from app.models import CharityProject
from app.services.google_api import calculate_collection_time
from app.schemas.charityproject import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):
    """CRUD-операции с благотворительными проектами."""

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Получить id проекта по его названию."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name,
            )
        )
        return db_project_id.scalars().first()

    async def get_charity_project_by_id(
            self,
            project_id: int,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        """Получить проект по id."""
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id
            )
        )
        return db_project.scalars().first()

    async def update_charity_project(
            self,
            db_project: CharityProject,
            project_in: CharityProjectUpdate,
            session: AsyncSession,
    ) -> CharityProject:
        """Обновить проект."""
        obj_data = jsonable_encoder(db_project)
        update_data = project_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_project, field, update_data[field])
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
        return db_project

    async def delete_charity_project(
            self,
            db_project: CharityProject,
            session: AsyncSession,
    ) -> CharityProject:
        """Удалить из БД проект."""
        await session.delete(db_project)
        await session.commit()
        return db_project

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, str]]:
        """Отсортировать список со всеми закрытыми проектами по кол-ву
        времени, понадобившемуся на сбор средств."""
        collection_time = await calculate_collection_time(
            create_date=CharityProject.create_date,
            close_date=CharityProject.close_date,
        )
        objects = await session.execute(
            select(
                CharityProject.name.label(NAME_LABEL),
                CharityProject.description.label(DESCRIPTION_LABEL),
                func.strftime(
                    COLLECTION_TIME_FORMAT,
                    collection_time,
                ).label(COLLECTION_TIME_LABEL),
            ).where(
                CharityProject.fully_invested == WAS_FULLY_INVESTED,
            ).order_by(collection_time)
        )
        return [dict(row) for row in objects]


charity_project_crud = CRUDCharityProject(CharityProject)
