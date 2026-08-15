from fastapi import APIRouter, Depends, status
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
    existing = None
    wa = payload.whatsapp_number.strip() if payload.whatsapp_number else None
    em = payload.email.strip() if payload.email else None
    name = payload.name.strip() if payload.name else None

    if em:
        result = await session.execute(select(Subscriber).where(Subscriber.email == em))
        existing = result.scalar_one_or_none()

    if not existing and wa:
        result = await session.execute(select(Subscriber).where(Subscriber.whatsapp_number == wa))
        existing = result.scalar_one_or_none()

    if existing:
        if name and not existing.name:
            existing.name = name
        if wa and not existing.whatsapp_number:
            existing.whatsapp_number = wa
        if em and not existing.email:
            existing.email = em
        await session.commit()
        await session.refresh(existing)
        return SubscriberResponse.model_validate(existing)

    subscriber = Subscriber(
        name=name,
        whatsapp_number=wa,
        email=em,
        source=payload.source or "website",
    )
    session.add(subscriber)
    await session.commit()
    await session.refresh(subscriber)
    return SubscriberResponse.model_validate(subscriber)
