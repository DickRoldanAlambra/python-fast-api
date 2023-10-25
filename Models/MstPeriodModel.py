from initializer import *

class PeriodBaseModel(BaseModel):
    Id: int
    Period: str
        
class Period(Base):
    __tablename__ = 'MstPeriod'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Period = Column(String(length=50))