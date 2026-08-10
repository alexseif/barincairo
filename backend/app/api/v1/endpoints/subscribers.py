from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.models.subscribers import Subscriber
from app.schemas.subscribers import SubscriberCreate, SubscriberResponse

router = APIRouter()


@router.post("/subscribers", response_model=SubscriberResponse, status_code=status.HTTP_201_CREATED)
async def create_subscriber(
    payload: SubscriberCreate,
    session: AsyncSession = Depends(get_async_session),
) -> SubscriberResponse:
    # Check if number already registered
    result = await session.execute(
        select(Subscriber).where(Subscriber.whatsapp_number == payload.whatsapp_number)
    )
    existing = result.scalar_one_or_none()
    if existing:
        return SubscriberResponse.model_validate(existing)

    subscriber = Subscriber(
        whatsapp_number=payload.whatsapp_number,
        source=payload.source or "website",
    )
    session.add(subscriber)
    await session.commit()
    await session.refresh(subscriber)
    return SubscriberResponse.model_validate(subscriber)
