from fastapi import APIRouter, HTTPException, Request
from services.google.email import getEmail 
from services.google.sheets import createSheet, updateSheet

router = APIRouter()

@router.get("/get-email/{emailId}")
async def getEmailId(req: Request, emailId: str):
    try:
        res = await getEmail(req.headers, emailId)
        success = {"status": "success"}
        success.update(res)
        return success
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/create-spreadsheet")
async def createSpreadsheet(req: Request):
    try:
        data = await req.json()
        res = await createSheet(req.headers, data)
        success = {"status": "success"}
        success.update(res)
        return success
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/update-spreadsheet")
async def updateSpreadsheet(req: Request):
    try:
        data = await req.json()
        # hardcoding spreadsheetid for now
        res = await updateSheet(req.headers, data, "1p_NpdRVzrZ6V51ZN3WJbvVvW8wZI-rabOLEiyyD4_dw")
        success = {"status": "success"}
        success.update(res)
        return success
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
