from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_user
from app.crud.charityproject import charity_project_crud
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)
from constants import ROUTE_CLEAR

router = APIRouter()


@router.post(
    ROUTE_CLEAR,
    response_model=list[dict[str, str]],
    dependencies=[Depends(current_user)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service),
):
    """Получить отчет c закрытми проектами, отсортированными
    по скорости сбора средств."""
    charity_projects = await (
        charity_project_crud.get_projects_by_completion_rate(session))
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid,
        charity_projects,
        wrapper_services,
    )
    return charity_projects
