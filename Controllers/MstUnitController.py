from initializer import *
import Models.MstUnitModel

session = SessionLocal()
router = APIRouter()

@router.get('/units')
async def get_all_units():
    try:
        # Get all unit instance
        units = session.query(Models.MstUnitModel.Unit).all()
        # Return all unit
        return units
    except Exception as e:
        # Handle any potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get('/unit/{id}')
async def get_unit_details(unit_id : int):
    try:
        # Get all unit instance
        unit = session.query(Models.MstUnitModel.Unit).get(unit_id)
        # Retrun the picked unit
        return unit
    except Exception as e:
        # Handle any potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get('/units/{search_filter}', response_model=List[Models.MstUnitModel.UnitBaseModel])
async def get_searched_units(search_filter : str):
    try:
        # Get all unit instance
        unit = session.query(Models.MstUnitModel.Unit).filter(Models.MstUnitModel.Unit.Unit == search_filter).all()
        # Retrun the picked unit
        return unit
    except Exception as e:
        # Handle any potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post('/add/unit/', response_model = Models.MstUnitModel.UnitBaseModel)
async def add_unit(unitModel : Models.MstUnitModel.UnitBaseModel):
    try:
        # Create a new Unit instance using the data from the request
        unit_to_add = Models.MstUnitModel.Unit(Unit=unitModel.Unit)
        # Add the unit to the session
        session.add(unit_to_add)
        # Commit the unit to the database
        session.commit()
        # Refresh the unit to get the database-generated ID
        session.refresh(unit_to_add)
        # Return the added unit
        return unit_to_add
    except Exception as e:
        # Handle any potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.put('/update/unit/{unit_id}', response_model = Models.MstUnitModel.UnitBaseModel)
async def update_unit(unit_id : int, unitModel : Models.MstUnitModel.UnitBaseModel):
    try:
        # Retrieve the unit to be updated by its ID
        unit_to_update = session.query(Models.MstUnitModel.Unit).filter(Models.MstUnitModel.Unit.Id == unit_id).first()

        if unit_to_update:
            # Update the unit's properties based on the provided data
            unit_to_update.Unit = unitModel.Unit
            # Commit the changes to the database
            session.commit()
            # Refresh the unit to ensure the latest data is returned
            session.refresh(unit_to_update)
            return unit_to_update
        else:
            # If the unit with the specified ID is not found, raise a 404 error
            raise HTTPException(status_code=404, detail=f"Unit with ID {unit_id} not found")
    except Exception as e:
        # Handle potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete('/delete/unit/{unit_id}')
async def delete_unit(unit_id : int):
    try:
        # Retrieve the unit to be deleted by its ID
        unit_to_delete = session.query(Models.MstUnitModel.Unit).filter(Models.MstUnitModel.Unit.Id == unit_id).first()

        if unit_to_delete:
            # Delete the unit from the session
            session.delete(unit_to_delete)
            # Commit the deletion to the database
            session.commit()
            return {"message": f"Unit with ID {unit_id} has been deleted"}
        else:
            # If the unit with the specified ID is not found, raise a 404 error
            raise HTTPException(status_code=404, detail=f"Unit with ID {unit_id} not found")
    except Exception as e:
        # Handle potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")      