// src/components/ContentScript.ts
import { getAuthToken } from "../chrome/utils";
import { parseEmailParts } from "../helpers/helperFn";

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
      
      // Fetch the full email details from Gmail
      const emailDetailsResponse = await fetch(
        `https://gmail.googleapis.com/gmail/v1/users/me/messages/${emailId}?format=full`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      const emailData = await emailDetailsResponse.json();
      console.log("Email Details:", emailData);
  
      // Parse email parts using your helper
      const emailDetails = parseEmailParts(emailData.payload.parts);
      console.log("Parsed Email Details:", emailDetails);
  
      // Convert the array of email details into a single string
      const emailContent = emailDetails.join(" ");
      const encodedEmailContent = encodeURIComponent(emailContent);
  
      // Call your backend endpoint passing both the email and token as query parameters
      const apiResponse = await fetch(
        `http://127.0.0.1:8080/company/company-job-info-crew-ai?email=${encodedEmailContent}&token=${token}`,
        { method: "POST" }
      );
  
      if (!apiResponse.ok) {
        throw new Error(`Backend error: ${apiResponse.status}`);
      }
  
      const responseData = await apiResponse.json();
      console.log("Response from backend:", responseData);
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
