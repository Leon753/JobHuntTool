import { useState } from "react";

import { getAuthToken } from "../chrome/utils";
import { parseEmailParts } from "../helpers/helperFn";
import CircularProgress from '@mui/material/CircularProgress';
import { Button } from "@mui/material";

const email_content = `Hi Mohammad Amin,

Thanks for your interest in the Avionics Hardware Engineer (Dragon) position at SpaceX. I have reviewed your resume and would like to arrange time for us to talk so I can learn more about your experience and interest in working at SpaceX.

To help schedule our call, select the "Enter your availability now" link at the very bottom of this email and block out several dates and times that you are available. The call will take about 30 minutes. Please note that times are displayed in your local time zone. Once I receive your response, I will confirm a time that works for both of us for the call.

Let me know if you have any questions. I look forward to hearing from you!

Thank you,`;

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
          properties: { title: "JobHuntingTest" }
      };

      const response = await fetch('http://127.0.0.1:8080/google/create-spreadsheet', {
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
  };

  const updateSpreadSheet = async (spreadsheetId: String) => {
    setLoading(true);
    try {
      const token = await getAuthToken();
      const spreadsheetUpdateResponse = await fetch(
        'http://127.0.0.1:8080/google/update-spreadsheet',
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
                  ["hi","Hunters"]
                ]
              }
            ],
            includeValuesInResponse: false,
            responseValueRenderOption: "FORMATTED_VALUE",
            responseDateTimeRenderOption: "SERIAL_NUMBER", 
            
          })
        }
      )
      console.log(spreadsheetUpdateResponse.status);
    } catch (err) {
      console.log(err);
      throw err;
    } finally {
      setLoading(false);
    };
  }
  const testEndPoint = async () => {
    setLoading(true);
    try {
      const token = await getAuthToken();
  
      // Build the payload using default/empty values for user_id and email_content
      const payload = {
        user_id: "123", // No value passed in
        email_content: email_content, // No value passed in
        
      };
  
      const spreadsheetUpdateResponse = await fetch(
        'http://127.0.0.1:8080/company/company-job-info-crew-ai',
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(payload)
        }
      );
  
      console.log(spreadsheetUpdateResponse.status);
    } catch (err) {
      console.error(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div>Hello. Let's start by fetching your emails</div>
      <Button onClick={fetchEmails}>Fetch Emails</Button>
      <Button onClick={createSpreadsheet}>Create Spreadsheet</Button>
      <Button onClick={testEndPoint}>Test Endpoint</Button>
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
