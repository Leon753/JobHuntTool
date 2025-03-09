// src/components/ContentScript.ts
import { getAuthToken } from "../chrome/utils";
import { parseEmailParts } from "../helpers/helperFn";

console.log("Content script loaded as module.");

/* ======================================================
   TYPES & INTERFACES
====================================================== */
export interface SpreadSheet {
  spreadsheetId: string;
}

export enum StatusEnum {
  Validated = "Validated",
  NeedsWork = "Needs Work",
}

export interface JobDetail {
  status: StatusEnum;
  content: String[];
  source: String[];
}

export interface JobResults {
  job_description: JobDetail;
  pay_range: JobDetail;
  interview_process: JobDetail;
  example_interview_experience: JobDetail;
}

export interface JobInfoResponse {
  data: {
    company: string;
    results: JobResults;
  };
}

/* ======================================================
   SPREADSHEET & TABLE FUNCTIONS
====================================================== */

/** Returns the first content value from each JobDetail in JobResults */
const getFirstIndexValues = (emailTable: JobResults | null): string[] => {
  if (!emailTable) return [];
  return Object.values(emailTable).map((detail) =>
    detail.content.length > 0 ? detail.content[0] : ""
  );
};

/** Updates spreadsheet data using the Sheets API */
const updateSpreadsheetData = async (
  token: string,
  spreadsheetId: string,
  values: string[]
): Promise<Response | null> => {
  try {
    const requestBody = {
      valueInputOption: "USER_ENTERED",
      data: [
        {
          range: "A1:E1",
          majorDimension: "ROWS",
          values: [values],
        },
      ],
      includeValuesInResponse: false,
      responseValueRenderOption: "FORMATTED_VALUE",
      responseDateTimeRenderOption: "SERIAL_NUMBER",
    };

    const response = await fetch(
      `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values:batchUpdate`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(requestBody),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response;
  } catch (error: any) {
    console.error("Error updating spreadsheet:", error);
    return null;
  }
};

/** Creates a new spreadsheet via the Sheets API */
const createNewSpreadsheet = async (
  token: string
): Promise<SpreadSheet | null> => {
  try {
    const requestBody = { properties: { title: "JobHunting" } };
    const response = await fetch("https://sheets.googleapis.com/v4/spreadsheets", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error: any) {
    console.error("Error creating spreadsheet:", error);
    return null;
  }
};

/** Calls your backend to generate a table from email details */
const generateTableRequest = async (
  emailDetails: String[]
): Promise<JobResults | null> => {
  try {
    const queryParam = encodeURIComponent(emailDetails.join(" "));
    const url = `http://127.0.0.1:8080/company/company-job-info-crew-ai?email=${queryParam}`;
    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const jsonData = await response.json();
    const parsedData = jsonData as JobInfoResponse;
    console.log("Career Table Data:", parsedData);
    return parsedData.data.results;
  } catch (err) {
    console.error("Error fetching career data:", err);
    return null;
  }
};

/* ======================================================
   GMAIL API CALLS & EMAIL HANDLING
====================================================== */

/** Extracts the email ID from the open email's DOM or URL */
const getEmailIdFromDOM = (): string | null => {
  const emailElement = document.querySelector("[data-legacy-message-id]");
  if (emailElement) {
    const emailId = emailElement.getAttribute("data-legacy-message-id");
    console.log("Extracted email ID from DOM:", emailId);
    return emailId;
  }
  const hash = window.location.hash;
  const match = hash.match(/#(?:inbox|all|sent)\/(.+)/);
  if (match) {
    console.log("Extracted email ID from URL:", match[1]);
    return match[1];
  }
  console.error("Email ID not found in DOM or URL.");
  return null;
};

/**
 * Fetches email details from the Gmail API and processes them
 * to update your spreadsheet.
 */
const handleFetchEmail = async (emailId: string) => {
  try {
    const token = await getAuthToken();
    const emailDetailsResponse = await fetch(
      `https://gmail.googleapis.com/gmail/v1/users/me/messages/${emailId}?format=full`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    const emailData = await emailDetailsResponse.json();
    console.log("Email Details:", emailData);

    const emailDetails = parseEmailParts(emailData.payload.parts);
    console.log("Parsed Email Details:", emailDetails);

    const emailTable = await generateTableRequest(emailDetails);
    console.log("Email Table:", emailTable);
    const spreadsheetCreationResponse = await createNewSpreadsheet(token);
    console.log("Spread Sheet Creation Response:", spreadsheetCreationResponse);

    // Use a local variable since content scripts don't require React state
    const spreadSheetId = (spreadsheetCreationResponse as SpreadSheet)?.spreadsheetId;
    console.log("SPREAD SHEET ID", spreadSheetId)
    if (!spreadSheetId) {
      console.error("Spreadsheet ID not available");
      return;
    }
    const values = getFirstIndexValues(emailTable);
    console.log("THESE ARE THE VALUES", values)
    const updateSpreadSheetResponse = await updateSpreadsheetData(token, spreadSheetId, values);
    console.log("UPDATE SPREASHEET RESPONSE", updateSpreadSheetResponse)
  } catch (error: any) {
    console.error("Error fetching email summary:", error.message);
  }
};

/* ======================================================
   DOM INJECTION
====================================================== */

/** Injects the "Fetch Email Summary" button after the email title */
const injectButtonWhenEmailOpened = () => {
  // Gmail usually displays the subject in an h2 with class "hP"
  const emailTitle = document.querySelector("h2.hP");
  if (emailTitle) {
    if (document.getElementById("fetch-email-summary-button")) {
      return;
    }
    const button = document.createElement("button");
    button.id = "fetch-email-summary-button";
    button.textContent = "Fetch Email Summary";
    button.style.marginBottom = "10px";
    button.style.fontSize = "14px";
    button.style.cursor = "pointer";

    button.addEventListener("click", async (event) => {
      event.stopPropagation();
      const emailId = getEmailIdFromDOM();
      if (emailId) {
        await handleFetchEmail(emailId);
      } else {
        console.error("Email ID extraction failed.");
      }
    });

    if (emailTitle.parentElement) {
      if (emailTitle.nextSibling) {
        emailTitle.parentElement.insertBefore(button, emailTitle.nextSibling);
      } else {
        emailTitle.parentElement.appendChild(button);
      }
    }
  } else {
    console.error("Email title element not found; cannot inject button after title.");
  }
};

// Set up a MutationObserver to check for changes in the Gmail view
const observer = new MutationObserver(() => {
  injectButtonWhenEmailOpened();
});
observer.observe(document.body, { childList: true, subtree: true });

// Initial injection attempt
injectButtonWhenEmailOpened();
