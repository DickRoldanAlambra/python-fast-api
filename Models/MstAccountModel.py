from initializer import *

class AccountBaseModel(BaseModel):
    Id: int
    Code: str
    Account: str
    IsLocked: bool
    AccountType: str
        
class Account(Base):
    __tablename__ = 'MstAccount'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String(length=50))
    Account = Column(String(length=100))
    IsLocked = Column(Boolean, default=False)
    AccountType: Column(String(length=50))
    __allow_unmapped__ = True

    