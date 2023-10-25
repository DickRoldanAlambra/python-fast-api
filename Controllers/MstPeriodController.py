from initializer import *
import Models.MstPeriodModel

session = SessionLocal()
router = APIRouter()

@router.get('/periods')
async def get_all_periods():
    try:
        # Get all periods instance
        periods = session.query(Models.MstPeriodModel.Period).all()
        # Return all periods
        return periods
    except Exception as e:
        # Handle any potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get('/period/{id}')
async def get_period_details(period_id : int):
    try:
        # Get all period instance
        period = session.query(Models.MstPeriodModel.Period).get(period_id)
        # Retrun the picked period
        return period
    except Exception as e:
        # Handle any potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get('/periods/{search_filter}', response_model=List[Models.MstPeriodModel.PeriodBaseModel])
async def get_searched_periods(search_filter : str):
    try:
        # Get all period instance
        period = session.query(Models.MstPeriodModel.Period).filter(Models.MstPeriodModel.Period.Period == search_filter).all()
        # Retrun the picked period
        return period
    except Exception as e:
        # Handle any potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post('/add/period/', response_model = Models.MstPeriodModel.PeriodBaseModel)
async def add_period(periodModel : Models.MstPeriodModel.PeriodBaseModel):
    try:
        # Create a new Period instance using the data from the request
        period_to_add = Models.MstPeriodModel.Period(Period=periodModel.Period)
        # Add the period to the session
        session.add(period_to_add)
        # Commit the period to the database
        session.commit()
        # Refresh the period to get the database-generated ID
        session.refresh(period_to_add)
        # Return the added period
        return period_to_add
    except Exception as e:
        # Handle any potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put('/update/period/{period_id}', response_model = Models.MstPeriodModel.PeriodBaseModel)
async def update_period(period_id : int, periodModel : Models.MstPeriodModel.PeriodBaseModel):
    try:
        # Retrieve the period to be updated by its ID
        period_to_update = session.query(Models.MstPeriodModel.Period).filter(Models.MstPeriodModel.Period.Id == period_id).first()

        if period_to_update:
            # Update the period's properties based on the provided data
            period_to_update.Period = periodModel.Period
            # Commit the changes to the database
            session.commit()
            # Refresh the period to ensure the latest data is returned
            session.refresh(period_to_update)
            return period_to_update
        else:
            # If the period with the specified ID is not found, raise a 404 error
            raise HTTPException(status_code=404, detail=f"Period with ID {period_id} not found")
    except Exception as e:
        # Handle potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete('/delete/period/{period_id}')
async def delete_period(period_id : int):
    try:
        # Retrieve the period to be deleted by its ID
        period_to_delete = session.query(Models.MstPeriodModel.Period).filter(Models.MstPeriodModel.Period.Id == period_id).first()

        if period_to_delete:
            # Delete the period from the session
            session.delete(period_to_delete)
            # Commit the deletion to the database
            session.commit()
            return {"message": f"Period with ID {period_id} has been deleted"}
        else:
            # If the period with the specified ID is not found, raise a 404 error
            raise HTTPException(status_code=404, detail=f"Unit with ID {period_id} not found")
    except Exception as e:
        # Handle potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")      