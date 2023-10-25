from initializer import *

class PayTypeBaseModel(BaseModel):
    Id: int
    PAYTYPECODE: str
    PayType: str
    AccountId: int
    SortNumber: int
        
class PayType(Base):
    __tablename__ = 'MstPayType'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    PAYTYPECODE = Column(String(length=50))
    PayType = Column(String(length=50))
    AccountId = Column(Integer, ForeignKey('MstAccount.id'))
