from fastapi import APIRouter, HTTPException
from models.user import UserAndExcelId
from services.user.user_service import save_user_info_to_db, get_user_excel_from_db, delete_user_info_from_db

router = APIRouter()

@router.post("/save-user-info")
async def save_user_info(user_info: UserAndExcelId):
    try:
        await save_user_info_to_db(user_info.user_id, user_info.excel_id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-user-excel")
async def get_user_excel(user_id: str):
    result = await get_user_excel_from_db(user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.delete("/delete-user-info")
async def delete_user_info(user_id: str):
    success = await delete_user_info_from_db(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "detail": f"User {user_id} deleted"}