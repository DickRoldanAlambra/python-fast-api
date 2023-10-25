from initializer import *
import Models.MstPayTypeModel
import Models.MstAccountModel

session = SessionLocal()
router = APIRouter()

@router.get('/paytypes')
async def get_all_paytypes():
    try:
      # Get all paytypes instances and join them with their associated accounts
        paytypes = (
            session.query(Models.MstPayTypeModel.PayType, Models.MstAccountModel.Account)
            .join(Models.MstAccountModel.Account, Models.MstPayTypeModel.PayType.AccountId == Models.MstAccountModel.Account.Id)
            .all()
        )
        paytype_account_data = []
        for paytype, account in paytypes:
            paytype_data = {
                "Id": paytype.Id,
                "PAYTYPECODE": paytype.PAYTYPECODE,
                "PayType": paytype.PayType,
                "AccountId": account.Id,
                "AccountType": account.Account
            }
            paytype_account_data.append(paytype_data)

        return paytype_account_data
    except Exception as e:
        # Handle any potential errors, such as database exceptions
        session.rollback()  # Roll back the transaction
        raise HTTPException(status_code=500, detail="Internal server error")