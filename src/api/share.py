from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List

engine = create_engine('postgresql://user:password@localhost/dbname')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class LabConfiguration(Base):
    __tablename__ = 'lab_configurations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    configuration = Column(String)

router = APIRouter()

@router.post('/lab-configurations')
def create_lab_configuration(name: str, configuration: str):
    session = Session()
    lab_configuration = LabConfiguration(name=name, configuration=configuration)
    session.add(lab_configuration)
    session.commit()
    return {'id': lab_configuration.id}

@router.get('/lab-configurations')
def get_lab_configurations():
    session = Session()
    lab_configurations = session.query(LabConfiguration).all()
    return [{'id': lab_configuration.id, 'name': lab_configuration.name} for lab_configuration in lab_configurations]

@router.get('/lab-configurations/{id}')
def get_lab_configuration(id: int):
    session = Session()
    lab_configuration = session.query(LabConfiguration).filter(LabConfiguration.id == id).first()
    if lab_configuration is None:
        raise HTTPException(status_code=404, detail='Lab configuration not found')
    return {'id': lab_configuration.id, 'name': lab_configuration.name, 'configuration': lab_configuration.configuration}

@router.put('/lab-configurations/{id}')
def update_lab_configuration(id: int, name: str, configuration: str):
    session = Session()
    lab_configuration = session.query(LabConfiguration).filter(LabConfiguration.id == id).first()
    if lab_configuration is None:
        raise HTTPException(status_code=404, detail='Lab configuration not found')
    lab_configuration.name = name
    lab_configuration.configuration = configuration
    session.commit()
    return {'id': lab_configuration.id, 'name': lab_configuration.name, 'configuration': lab_configuration.configuration}

@router.delete('/lab-configurations/{id}')
def delete_lab_configuration(id: int):
    session = Session()
    lab_configuration = session.query(LabConfiguration).filter(LabConfiguration.id == id).first()
    if lab_configuration is None:
        raise HTTPException(status_code=404, detail='Lab configuration not found')
    session.delete(lab_configuration)
    session.commit()
    return {'id': id}