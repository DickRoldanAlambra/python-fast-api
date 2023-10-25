from initializer import *

class UnitBaseModel(BaseModel):
    Id: int
    Unit: str
        
class Unit(Base):
    __tablename__ = 'MstUnit'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Unit = Column(String(length=50))