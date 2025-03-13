// src/components/ContentScript.ts
import { createEmitAndSemanticDiagnosticsBuilderProgram } from "typescript";
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

const handleFetchEmail = async (emailId: string) => {
  try {
    const token = await getAuthToken();
    const emailDetailsResponse = await fetch(
      `http://127.0.0.1:8080/google/get-email/${emailId}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    const emailData = await emailDetailsResponse.json();


    console.log("Email Details:", emailData);
    const emailDetails = parseEmailParts(emailData.payload.parts) ;
    const payload = {
        user_id: emailData.payload.headers[0].value,
        email_content: emailDetails[0]
    }
    console.log(payload)
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
  } catch (error: any) {
    console.error("Error fetching email summary:", error.message);
  }
};

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
