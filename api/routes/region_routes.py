from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///region_restrictions.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)

router = APIRouter()

class RegionRestrictionRequest(BaseModel):
    region: str

@router.post("/region/restrictions")
async def create_region_restriction(request: RegionRestrictionRequest, session: Session = Depends(Session)):
    region = session.query(Region).filter(Region.name == request.region).first()
    if region:
        return {"message": f"Region {request.region} already exists"}
    else:
        new_region = Region(name=request.region)
        session.add(new_region)
        session.commit()
        return {"message": f"Region {request.region} created"}

@router.get("/region/restrictions")
async def get_region_restrictions(session: Session = Depends(Session)):
    regions = session.query(Region).all()
    return {"regions": [region.name for region in regions]}

@router.delete("/region/restrictions/{region_id}")
async def delete_region_restriction(region_id: int, session: Session = Depends(Session)):
    region = session.query(Region).filter(Region.id == region_id).first()
    if region:
        session.delete(region)
        session.commit()
        return {"message": f"Region {region.name} deleted"}
    else:
        raise HTTPException(status_code=404, detail="Region not found")

@router.get("/region/restrictions/enabled")
async def get_enabled_regions(session: Session = Depends(Session)):
    enabled_regions = session.query(Region).filter(Region.enabled == True).all()
    return {"enabled_regions": [region.name for region in enabled_regions]}

@router.post("/region/restrictions/enabled")
async def enable_region_restriction(region: str, session: Session = Depends(Session)):
    region = session.query(Region).filter(Region.name == region).first()
    if region:
        region.enabled = True
        session.commit()
        return {"message": f"Region {region.name} enabled"}
    else:
        return {"message": f"Region {region} not found"}

@router.delete("/region/restrictions/enabled/{region_id}")
async def disable_region_restriction(region_id: int, session: Session = Depends(Session)):
    region = session.query(Region).filter(Region.id == region_id).first()
    if region:
        region.enabled = False
        session.commit()
        return {"message": f"Region {region.name} disabled"}
    else:
        raise HTTPException(status_code=404, detail="Region not found")