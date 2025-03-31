
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.create_table import Columns, ColumnResult, PayRange_ColumnResult, JobInformation
from models.email_summary import GPT_Email_Summary_Response, Status
from utils.helpers import extract_row_values

@pytest.fixture
def sample_columns():
    return Columns(
        job_description=ColumnResult(
            status="Validated",
            content=["Worked on low-level firmware", "Collaborated with EE team"],
            source=["https://example.com/jd"]
        ),
        pay_range=PayRange_ColumnResult(
            status="Validated",
            content=[{"position": "Hardware Engineer", "salary": "120-140k"}],
            source=["https://levels.fyi"]
        ),
        interview_process=ColumnResult(
            status="Validated",
            content=["Initial HR screen", "Technical interview", "Final panel"],
            source=["https://example.com/interview"]
        ),
        example_interview_experience=ColumnResult(
            status="Needs Work",
            content=["Challenging but fair", "Technical questions focused on C++"],
            source=[]
        ),
        career_growth=ColumnResult(
            status="Validated",
            content=["Good opportunities for advancement"],
            source=[]
        ),
        example_technical_questions=ColumnResult(
            status="Validated",
            content=["Implement a circular buffer", "Explain memory alignment"],
            source=[]
        )
    )

@pytest.fixture
def sample_summary_response():
    return GPT_Email_Summary_Response(
        company="SpaceX",
        job_position="Hardware Engineer",
        status=Status.INTERVIEWING , # Make sure Status is an Enum
        summary="Interview scheduled for next week.",
    )

@pytest.fixture
def sample_job_info(sample_summary_response:GPT_Email_Summary_Response, sample_columns):
    return JobInformation(
        company=sample_summary_response.company,
        results=sample_columns
    )

def test_extract_row_helpers(sample_job_info:JobInformation, sample_summary_response:GPT_Email_Summary_Response):
    print(sample_job_info.results)
    row = extract_row_values(sample_job_info, sample_summary_response)
    assert row[0] == "SpaceX"
    assert row[1] == "Hardware Engineer"
    assert row[2] == str(Status.INTERVIEWING.value)
    assert row[3].startswith("*Worked on low-level firmware")
    assert row[4].startswith("*Hardware Engineer: 120-140k")
    assert row[5].startswith("*Initial HR screen")
    assert row[6].startswith("*Challenging but fair")
    assert row[7].startswith("*Good opportunities for advancement")
    assert row[8].startswith("*Implement a circular buffer")
    