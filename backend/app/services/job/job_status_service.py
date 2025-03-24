from fastapi import HTTPException
from models.create_table import JobInformation
from models.email_summary import GPT_Email_Summary_Response
from config.logger import logger
from services.sheets import sheets_service
from services.user import user_service
from utils.helpers import extract_row_values
from services.job import job_info_service

async def handle_in_review_or_interview(
    summary_json: GPT_Email_Summary_Response,
    user_id: str,
    authorization: str
) -> None:
    query_key = summary_json.company + summary_json.job_position+" " +" " + " " + " "
    # 1) Get or create job info (from memo or CrewAI)
    response: JobInformation = await job_info_service.get_or_create_job_info(query_key, summary_json)

    # 2) Check if user has an existing sheet
    user_service_response = await user_service.get_user_excel_from_db(user_id=user_id)
    if user_service_response is None:
        # Create new sheet & store in DB
        excel_id, start_row = await sheets_service.create_new_sheet_for_user(
            authorization,
            user_id,
            title="JOBHUNT"
        )
        await user_service.save_user_info_to_db(
            user_id=user_id,
            current_sheet_row=start_row,
            excel_id=excel_id
        )
        # Optionally apply formatting
        await sheets_service.apply_sheet_formatting(authorization, excel_id)
        row = start_row
    else:
        row = user_service_response["current_sheet_row"]
        excel_id = user_service_response["excel_id"]

    # 3) Update the sheet with the new row
    row_values = extract_row_values(response, summary_json)  # A helper that turns JobInformation -> list
    await sheets_service.update_google_sheets_row(
        authorization,
        user_id,
        excel_id,
        row,
        row_values
    )

    # 4) Update DB to reflect the new row usage
    await user_service.update_user_row(user_id=user_id, current_sheet_row=row+1)

    # 5) (Optional) re-apply formatting each time, if needed
    await sheets_service.apply_sheet_formatting(authorization, excel_id)

    # 6) Save job & sheet row reference in DB
    await user_service.save_excel_job_row_to_db(
        user_id=user_id,
        company=summary_json.company,
        position=summary_json.job_position,
        sheet_row=row
    )

async def handle_offer_or_rejection(
    summary_json: GPT_Email_Summary_Response,
    user_id: str,
    authorization: str
) -> str:
    user_service_response = await user_service.get_user_excel_from_db(user_id=user_id)
    if not user_service_response:
        raise HTTPException(status_code=404, detail="No spreadsheet found for user")

    excel_id = user_service_response["excel_id"]
    row = await user_service.get_excel_job_row_from_db(
        user_id=user_id,
        company=summary_json.company,
        position=summary_json.job_position
    )
    # Update just the status column
    await sheets_service.update_status_column(
        authorization,
        user_id,
        excel_id,
        row,
        [str(summary_json.status.name)]
    )
    return "UPDATE DATABASE"