from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from modules.database.models import Farm, User, user_farm
from modules.database.schemas.user_farm_schemas import (
    FarmCreateRequest,
    FarmResponse,
    FarmUpdateRequest,
)
from modules.utilities.auth import get_current_user, get_db_session

router = APIRouter(tags=["Farms"])


@router.post("/farms", response_model=FarmResponse)
async def create_farm(
    request: FarmCreateRequest,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),  # noqa: B950
):
    # Create a new Farm instance
    new_farm = Farm(
        name=request.name,
        latitude=request.latitude,
        longitude=request.longitude,
        size=request.size,
        users=[current_user],
    )

    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    # Create the association in the user_farm table

    # Return the created farm details
    return FarmResponse(
        id=new_farm.id,
        name=new_farm.name,
        latitude=new_farm.latitude,
        longitude=new_farm.longitude,
        size=new_farm.size,
        created_at=new_farm.created_at,
        updated_at=new_farm.updated_at,
    )


@router.delete("/farms/{farm_id}", response_model=FarmResponse)
async def delete_farm(
    farm_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)
):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    # Check if the current user has access to the farm
    user_farm_relation = (
        db.query(user_farm)
        .filter(user_farm.c.user_id == current_user.id, user_farm.c.farm_id == farm_id)
        .first()  # noqa: B950
    )

    if not user_farm_relation:
        raise HTTPException(status_code=403, detail="You don't have access to this farm")

    db.delete(farm)
    db.commit()

    return FarmResponse(
        id=farm.id,
        name=farm.name,
        latitude=farm.latitude,
        longitude=farm.longitude,
        size=farm.size,
        created_at=farm.created_at,
        updated_at=farm.updated_at,
    )


@router.get("/farms/{farm_id}", response_model=FarmResponse)
async def get_farm_by_id(
    farm_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)
):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    # Check if the current user has access to the farm
    user_farm_relation = (
        db.query(user_farm)
        .filter(user_farm.c.user_id == current_user.id, user_farm.c.farm_id == farm_id)
        .first()  # noqa: B950
    )

    if not user_farm_relation:
        raise HTTPException(status_code=403, detail="You don't have access to this farm")

    return FarmResponse(
        id=farm.id,
        name=farm.name,
        latitude=farm.latitude,
        longitude=farm.longitude,
        size=farm.size,
        created_at=farm.created_at,
        updated_at=farm.updated_at,
    )


@router.get("/farms", response_model=List[FarmResponse])
async def list_all_farms(
    db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)
):  # noqa: B950
    farms = db.query(Farm).join(user_farm).filter(user_farm.c.user_id == current_user.id).all()  # noqa: B950

    return [
        FarmResponse(
            id=farm.id,
            name=farm.name,
            latitude=farm.latitude,
            longitude=farm.longitude,
            size=farm.size,
            created_at=farm.created_at,
            updated_at=farm.updated_at,
        )
        for farm in farms
    ]


@router.put("/farms/{farm_id}", response_model=FarmResponse)
async def update_farm(
    farm_id: int,
    request: FarmUpdateRequest,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    # Check if the current user has access to the farm
    user_farm_relation = (
        db.query(user_farm)
        .filter(user_farm.c.user_id == current_user.id, user_farm.c.farm_id == farm_id)
        .first()  # noqa: B950
    )

    if not user_farm_relation:
        raise HTTPException(status_code=403, detail="You don't have access to this farm")  # noqa: B950

    # Update the farm details
    if request.name is not None:
        farm.name = request.name
    if request.latitude is not None:
        farm.latitude = request.latitude
    if request.longitude is not None:
        farm.longitude = request.longitude
    if request.size is not None:
        farm.size = request.size

    farm.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(farm)

    return FarmResponse(
        id=farm.id,
        name=farm.name,
        latitude=farm.latitude,
        longitude=farm.longitude,
        size=farm.size,
        created_at=farm.created_at,
        updated_at=farm.updated_at,
    )
