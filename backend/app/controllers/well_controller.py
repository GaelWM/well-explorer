from typing import List, Optional
from sqlalchemy.orm import Session # type: ignore
from fastapi import HTTPException # type: ignore

from app.repositories.well_repository import WellRepository
from app.schemas.well_schema import Well, WellCreate, WellUpdate

class WellController:
    @staticmethod
    def get_wells(db: Session, skip: int = 0, limit: int = 100) -> List[Well]:
        return WellRepository.get_wells(db, skip, limit)

    @staticmethod
    def get_well_by_id(db: Session, well_id: int) -> Well:
        db_well = WellRepository.get_well_by_id(db, well_id)
        if not db_well:
            raise HTTPException(status_code=404, detail=f"Well with id {well_id} not found")
        return db_well

    @staticmethod
    def create_well(db: Session, well: WellCreate) -> Well: 
        db_well = WellRepository.get_well_by_name(db, name=well.name)
        if db_well:
            raise HTTPException(status_code=400, detail=f"Well with name {well.name} already exists")
        return WellRepository.create_well(db, well)

    @staticmethod
    def update_well(db: Session, well_id: int, well_update: WellUpdate) -> Well:
        db_well = WellRepository.update_well(db, well_id, well_update)
        if not db_well:
            raise HTTPException(status_code=404, detail=f"Well with id {well_id} not found")
        return db_well

    @staticmethod
    def delete_well(db: Session, well_id: int) -> dict:
        success = WellRepository.delete_well(db, well_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Well with id {well_id} not found")
        return {"message": f"Well with id {well_id} deleted successfully"}
        
    @staticmethod
    def get_wells_by_region(db: Session, region: str) -> List[Well]:
        wells = WellRepository.get_wells_by_region(db, region)
        if not wells:
            raise HTTPException(status_code=404, detail=f"No wells found in region {region}")
        return wells
    

    @staticmethod
    def get_wells_by_depth(db: Session, depth: int) -> List[str]:
        wellNames = WellRepository.get_wells_by_depth(db, depth)
        if not wellNames:
            raise HTTPException(status_code=404, detail=f"No wells found with depth greater than {depth}")
        return wellNames