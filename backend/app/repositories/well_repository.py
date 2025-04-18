from typing import List, Optional
from sqlalchemy.orm import Session # type: ignore

from app.models.well import Well
from backend.app.schemas.well_schema import WellCreate, WellUpdate

class WellRepository:
    @staticmethod
    def get_wells(db: Session, skip: int = 0, limit: int = 100) -> List[Well]:
        return db.query(Well).offset(skip).limit(limit).all()

    @staticmethod
    def get_well_by_id(db: Session, well_id: int) -> Optional[Well]:
        return db.query(Well).filter(Well.id == well_id).first()

    @staticmethod
    def get_well_by_name(db: Session, name: str) -> Optional[Well]:
        return db.query(Well).filter(Well.name == name).first()

    @staticmethod
    def create_well(db: Session, well: WellCreate) -> Well:
        db_well = Well(
            name=well.name,
            latitude=well.latitude,
            longitude=well.longitude,
            lift_type=well.lift_type,
            region=well.region,
            installation_date=well.installation_date
        )
        db.add(db_well)
        db.commit()
        db.refresh(db_well)
        return db_well

    @staticmethod
    def update_well(db: Session, well_id: int, well_update: WellUpdate) -> Optional[Well]:
        db_well = WellRepository.get_well_by_id(db, well_id)
        if not db_well:
            return None
            
        update_data = well_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_well, field, value)
            
        db.commit()
        db.refresh(db_well)
        return db_well

    @staticmethod
    def delete_well(db: Session, well_id: int) -> bool:
        db_well = WellRepository.get_well_by_id(db, well_id)
        if not db_well:
            return False
            
        db.delete(db_well)
        db.commit()
        return True
        
    @staticmethod
    def get_wells_by_region(db: Session, region: str) -> List[Well]:
        return db.query(Well).filter(Well.region == region).all()