from initializer import *
import Models.MstPeriodModel

session = SessionLocal()
router = APIRouter()

@router.get('/periods')
async def all():
    try:
        periods = session.query(Models.MstPeriodModel.Period).all()
        return periods
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get('/period/{id}')
async def one(id : int):
    try:
        period = session.query(Models.MstPeriodModel.Period).get(id)
        return period
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get('/periods/{search}', response_model=List[Models.MstPeriodModel.PeriodBaseModel])
async def search(search : str):
    try:
        period = session.query(Models.MstPeriodModel.Period).filter(Models.MstPeriodModel.Period.Period == search).all()
        return period
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post('/add/period/', response_model = Models.MstPeriodModel.PeriodBaseModel)
async def save(periodModel : Models.MstPeriodModel.PeriodBaseModel):
    try:
        period_to_add = Models.MstPeriodModel.Period(Period=periodModel.Period)
        session.add(period_to_add)
        session.commit()
        session.refresh(period_to_add)
        return period_to_add
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put('/update/period/{id}', response_model = Models.MstPeriodModel.PeriodBaseModel)
async def update(id : int, periodModel : Models.MstPeriodModel.PeriodBaseModel):
    try:
        period_to_update = session.query(Models.MstPeriodModel.Period).filter(Models.MstPeriodModel.Period.Id == id).first()

        if period_to_update:
            period_to_update.Period = periodModel.Period
            session.commit()
            session.refresh(period_to_update)
            return period_to_update
        else:
            raise HTTPException(status_code=404, detail=f"Period with ID {id} not found")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete('/delete/period/{id}')
async def remove(id : int):
    try:
        period_to_delete = session.query(Models.MstPeriodModel.Period).filter(Models.MstPeriodModel.Period.Id == id).first()

        if period_to_delete:
            session.delete(period_to_delete)
            session.commit()
            return {"message": f"Period with ID {id} has been deleted"}
        else:
            raise HTTPException(status_code=404, detail=f"Unit with ID {id} not found")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
