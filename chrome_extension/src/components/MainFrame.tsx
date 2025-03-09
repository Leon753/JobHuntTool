import { useState } from "react";

import { getAuthToken } from "../chrome/utils";
import { parseEmailParts } from "../helpers/helperFn";
import CircularProgress from '@mui/material/CircularProgress';
import { Button } from "@mui/material";

interface Props {}

type Email = {
  id: string
}

type SpreadSheet = {
  spreadsheetId: string
}

export enum StatusEnum {
  Validated = "Validated",
  NeedsWork = "Needs Work",
}

export interface JobResults {
  job_description: JobDetail;
  pay_range: JobDetail;
  interview_process: JobDetail;
  example_interview_experience: JobDetail;
}

export interface JobDetail {
  status: StatusEnum; // Define valid statuses
  content: String[];
  source: String[];
}

export interface JobInfoResponse {
  data: {
      company: string;
      results: JobResults;
  };
}


const getFirstIndexValues = (emailTable: JobResults | null): string[] => {
  if (!emailTable) return [];

  const firstIndexValues: string[] = [];

  for (const value of Object.values(emailTable)) {
      if (value.content.length > 0) {
          firstIndexValues.push(value.content[0]); // Get first index of each field
      } else {
          firstIndexValues.push(""); // Placeholder if content is empty
      }
  }

  return firstIndexValues;
};


const generateTableRequest = async (emailDetails: String[]): Promise<JobResults | null> => {
  try {
      const queryParam = encodeURIComponent(emailDetails.join(" "));
      const url = `http://127.0.0.1:8080/company/company-job-info-crew-ai?email=${queryParam}`;

      const response = await fetch(url, {
          method: "GET",
          headers: {
              "Content-Type": "application/json"
          }
      });

      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const jsonData = await response.json();

      // Type assertion with validation
      const parsedData = jsonData as JobInfoResponse;

      console.log("Career Table Data:", parsedData);

      return parsedData.data.results; // Return the extracted `JobResults` object
  } catch (err) {
      console.error("Error fetching career data:", err);
      return null;
  }
};


const createNewSpreadsheet = async (token: string): Promise<SpreadSheet | null> => {
  try {
      const requestBody = {
          properties: { title: "JobHunting" }
      };

      const response = await fetch('https://sheets.googleapis.com/v4/spreadsheets', {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      return await response.json(); // Returns the parsed spreadsheet object
  } catch (error: any) {
      console.error("Error creating spreadsheet:", error);
      // setError(error.message);
      return null;
  }
};

const updateSpreadsheetData = async (token: string, spreadsheetId: String, values:String[]): Promise<Response | null> => {
  try {
      const requestBody = {
          valueInputOption: "USER_ENTERED",
          data: [
              {
                  range: "A1:D1",
                  majorDimension: "ROWS",
                  values: [values],
              }
          ],
          includeValuesInResponse: false,
          responseValueRenderOption: "FORMATTED_VALUE",
          responseDateTimeRenderOption: "SERIAL_NUMBER"
      };

      const response = await fetch(
          `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values:batchUpdate`,
          {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${token}`
              },
              body: JSON.stringify(requestBody)
          }
      );

      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      return response;
  } catch (error: any) {
      console.error("Error updating spreadsheet:", error);
      // setError(error.message);
      return null;
  }
};


function MainFrame() {
  const [emailSummaryData, setEmailSummaryData] = useState<String[]>([]);
  const [careerTable, setCareerTable] = useState<JobResults | null>(null);
  const [spreadSheetId, setSpreadSheetID] = useState<String>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchEmails = async () => {
    setLoading(true);
    setError(null);

    try {
      const token = await getAuthToken();
      const emailResponse = await fetch(
          "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=1&q=subject:Application",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
      );
      const data = await emailResponse.json();
      console.log("Emails:", data);

      if (data.messages.length > 0) {
        const emailDetailsResponses = await fetch(
          `https://gmail.googleapis.com/gmail/v1/users/me/messages/${(data.messages[0] as Email).id}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        const emailData = await emailDetailsResponses.json();
        console.log("Email Details: ", emailData);

        const emailDetails = parseEmailParts(emailData.payload.parts) ;
        console.log(emailDetails);


        const emailTable = await generateTableRequest(emailDetails);
        const spreadsheetCreationResponse = await createNewSpreadsheet(token);
    
        
        setCareerTable(emailTable);
        setSpreadSheetID((spreadsheetCreationResponse as SpreadSheet).spreadsheetId);
        const values =  getFirstIndexValues(emailTable)
        
        
        const updateSpreadSheetReponse = await updateSpreadsheetData(token, spreadSheetId, values)

        console.log("Email Table:");
        console.log(emailTable);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };


  const createSpreadsheet = async () => {
    setLoading(true);
    
    try {
      const token = await getAuthToken();
      const spreadsheetCreationResponse = await createNewSpreadsheet(token);
      setSpreadSheetID((spreadsheetCreationResponse as SpreadSheet).spreadsheetId);
      return spreadsheetCreationResponse;
    } catch (err) {
      // TODO (developer) - Handle exception
      throw err;
    } finally {
      setLoading(false);
    }
  }

  const updateSpreadSheet = async (spreadsheetId: String) => {
    setLoading(true);
    try {
      const token = await getAuthToken();
      const spreadsheetUpdateResponse = await fetch(
        `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values:batchUpdate`,
        {
          method: "POST",
          headers: {
           "Content-Type": 'application/json',
           Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            valueInputOption: "USER_ENTERED",
            data: [
              {
                range: "A1:B1",
                majorDimension: "ROWS",
                values: [
                  ["hi","JobHunter"]
                ]
              }
            ],
            includeValuesInResponse: false,
            responseValueRenderOption: "FORMATTED_VALUE",
            responseDateTimeRenderOption: "SERIAL_NUMBER"
          })
        }
      )
      console.log(spreadsheetUpdateResponse.status);
    } catch (err) {
      console.log(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div>Hello. Let's start by fetching your emails</div>
      <Button onClick={fetchEmails}>Fetch Emails</Button>
      <Button onClick={createSpreadsheet}>Create Spreadsheet</Button>
      <Button onClick={() => updateSpreadSheet(spreadSheetId)}>Update Spreadsheet</Button>
      <>
      {
        loading ? 
        <CircularProgress /> : <>{emailSummaryData}</>
      }</>
      <p>{spreadSheetId}</p>
    </>
  );
}

export default MainFrame;
