from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investment_process import investition
from constants import ROUTE_CLEAR, ROUTE_MY

router = APIRouter()


@router.post(
    ROUTE_CLEAR,
    response_model=DonationDB,
    response_model_exclude={
        'user_id', 'fully_invested', 'invested_amount',
    },
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создать пожертвование."""
    new_donation = await donation_crud.create(
        donation, session, user,
    )
    projects = await charity_project_crud.free_objects(session)
    await investition(
        main_value=new_donation,
        values=projects,
        session=session,
    )
    return new_donation


@router.get(
    ROUTE_CLEAR,
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude={'close_date'},
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> list[DonationDB]:
    """Получить список всех пожертвований (Только для суперюзеров)."""
    return await donation_crud.get_multi(session)


@router.get(
    ROUTE_MY,
    response_model=list[DonationDB],
    response_model_exclude={
        'user_id', 'fully_invested', 'invested_amount', 'close_date',
    },
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получить список всех пожертвований для текущего пользователя."""
    return await donation_crud.get_donations_by_user(
        session=session, user=user,
    )
