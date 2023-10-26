from initializer import *
import Models.MstUnitModel

session = SessionLocal()
router = APIRouter()

@router.get('/units')
async def all():
    try:
        units = session.query(Models.MstUnitModel.Unit).all()
        return units
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get('/unit/{id}')
async def one(id : int):
    try:
        unit = session.query(Models.MstUnitModel.Unit).get(id)
        return unit
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get('/units/{search}', response_model=List[Models.MstUnitModel.UnitBaseModel])
async def search(search : str):
    try:
        unit = session.query(Models.MstUnitModel.Unit).filter(Models.MstUnitModel.Unit.Unit == search).all()
        return unit
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post('/add/unit/', response_model = Models.MstUnitModel.UnitBaseModel)
async def save(unitModel : Models.MstUnitModel.UnitBaseModel):
    try:
        unit_to_add = Models.MstUnitModel.Unit(Unit=unitModel.Unit)
        session.add(unit_to_add)
        session.commit()
        session.refresh(unit_to_add)
        return unit_to_add
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.put('/update/unit/{id}', response_model = Models.MstUnitModel.UnitBaseModel)
async def update(id : int, unitModel : Models.MstUnitModel.UnitBaseModel):
    try:
        unit_to_update = session.query(Models.MstUnitModel.Unit).filter(Models.MstUnitModel.Unit.Id == id).first()

        if unit_to_update:
            unit_to_update.Unit = unitModel.Unit
            session.commit()
            session.refresh(unit_to_update)
            return unit_to_update
        else:
            raise HTTPException(status_code=404, detail=f"Unit with ID {id} not found")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete('/delete/unit/{id}')
async def remove(id : int):
    try:
        unit_to_delete = session.query(Models.MstUnitModel.Unit).filter(Models.MstUnitModel.Unit.Id == id).first()

        if unit_to_delete:
            session.delete(unit_to_delete)
            session.commit()
            return {"message": f"Unit with ID {id} has been deleted"}
        else:
            raise HTTPException(status_code=404, detail=f"Unit with ID {id} not found")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
