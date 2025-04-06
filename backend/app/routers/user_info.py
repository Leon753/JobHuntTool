from config.logger import logger
from services.sheets.sheets_service import create_new_sheet_for_user
from fastapi import APIRouter, HTTPException, Request
from models.user import UserAndExcelId
from services.user.user_service import save_user_info_to_db, get_user_excel_from_db, delete_user_info_from_db

router = APIRouter()

@router.post("/save-user-info")
async def save_user_info(user_info: UserAndExcelId):
    try:
        # save should start at row 2.
        await save_user_info_to_db(user_info.user_id, 2, user_info.excel_id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-user-excel")
async def get_user_excel(req: Request, user_id: str):
    result = await get_user_excel_from_db(user_id)
    if result is None:
        # if no excel sheet found. Create one for the user and set this up.
        excel_id, start_row = await create_new_sheet_for_user(req.headers.get("authorization"), user_id, "JOBHUNT")
        return {"current_sheet_row": start_row, "excel_id": excel_id, "user_id": user_id}
    
    return result

@router.delete("/delete-user-info")
async def delete_user_info(user_id: str):
    success = await delete_user_info_from_db(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "detail": f"User {user_id} deleted"}
