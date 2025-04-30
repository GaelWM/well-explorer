from typing import List
from fastapi import APIRouter, Depends, Query # type: ignore
from sqlalchemy.orm import Session # type: ignore

from app.core.database import get_db
from app.controllers.well_controller import WellController
from app.schemas.well_schema import Well, WellCreate, WellUpdate

router = APIRouter()

@router.get("/", response_model=List[Well])
def get_wells(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Retrieve wells with pagination.
    """
    return WellController.get_wells(db, skip=skip, limit=limit)

@router.get("/{well_id}", response_model=Well)
def get_well(well_id: int, db: Session = Depends(get_db)):
    """
    Get a specific well by ID.
    """
    return WellController.get_well_by_id(db, well_id=well_id)

@router.post("/", response_model=Well)
def create_well(well: WellCreate, db: Session = Depends(get_db)):
    """
    Create a new well.
    """
    return WellController.create_well(db, well=well)

@router.put("/{well_id}", response_model=Well)
def update_well(well_id: int, well_update: WellUpdate, db: Session = Depends(get_db)):
    """
    Update a well.
    """
    return WellController.update_well(db, well_id=well_id, well_update=well_update)

@router.delete("/{well_id}")
def delete_well(well_id: int, db: Session = Depends(get_db)):
    """
    Delete a well.
    """
    return WellController.delete_well(db, well_id=well_id)

@router.get("/region/{region}", response_model=List[Well])
def get_wells_by_region(region: str, db: Session = Depends(get_db)):
    """
    Get wells by region.
    """
    return WellController.get_wells_by_region(db, region=region)

@router.get('/depth/{depth}', response_model=List[str])
def get_wells_by_depth(depth: int, db: Session = Depends(get_db)):
    return WellController.get_wells_by_depth(db, depth)

