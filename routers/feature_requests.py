from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dependencies import get_db
from limiter import limiter
from models import FeatureRequest
from dtos.requests.feature_request import FeatureRequestCreate, FeatureRequestUpdate
from dtos.responses.feature_request import FeatureRequestResponse

router = APIRouter(tags=["feature_requests"])


@router.post("/feature-requests", response_model=FeatureRequestResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_feature_request(request: Request, data: FeatureRequestCreate, db: AsyncSession = Depends(get_db)):
    feature_request = FeatureRequest(
        title=data.title,
        category=data.category,
        description=data.description,
    )
    db.add(feature_request)
    await db.commit()
    await db.refresh(feature_request)
    return feature_request


@router.get("/feature-requests", response_model=List[FeatureRequestResponse])
async def list_feature_requests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FeatureRequest).order_by(FeatureRequest.votes.desc()))
    return result.scalars().all()


@router.get("/feature-requests/{feature_request_id}", response_model=FeatureRequestResponse)
async def get_feature_request(feature_request_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FeatureRequest).where(FeatureRequest.id == feature_request_id))
    feature_request = result.scalar_one_or_none()
    if feature_request is None:
        raise HTTPException(status_code=404, detail="Feature request not found")
    return feature_request


@router.patch("/feature-requests/{feature_request_id}", response_model=FeatureRequestResponse)
async def update_feature_request(feature_request_id: int, update: FeatureRequestUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FeatureRequest).where(FeatureRequest.id == feature_request_id))
    feature_request = result.scalar_one_or_none()
    if feature_request is None:
        raise HTTPException(status_code=404, detail="Feature request not found")

    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(feature_request, field, value)

    await db.commit()
    await db.refresh(feature_request)
    return feature_request


@router.post("/feature-requests/{feature_request_id}/vote", response_model=FeatureRequestResponse)
@limiter.limit("10/minute")
async def vote_feature_request(request: Request, feature_request_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FeatureRequest).where(FeatureRequest.id == feature_request_id))
    feature_request = result.scalar_one_or_none()
    if feature_request is None:
        raise HTTPException(status_code=404, detail="Feature request not found")

    feature_request.votes = FeatureRequest.votes + 1
    await db.commit()
    await db.refresh(feature_request)
    return feature_request


@router.delete("/feature-requests/{feature_request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feature_request(feature_request_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FeatureRequest).where(FeatureRequest.id == feature_request_id))
    feature_request = result.scalar_one_or_none()
    if feature_request is None:
        raise HTTPException(status_code=404, detail="Feature request not found")

    await db.delete(feature_request)
    await db.commit()
    return None
