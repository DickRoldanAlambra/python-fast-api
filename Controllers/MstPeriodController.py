from initializer import *
import Models.MstPeriodModel

session = SessionLocal()
router = APIRouter()

@router.get('/periods')
async def get_periods():
    periods = session.query(Models.MstPeriodModel.Period).all()
    return periods