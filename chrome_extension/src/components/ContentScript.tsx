// src/components/ContentScript.ts
import { getAuthToken } from "../chrome/utils";

console.log("Content script loaded as module.");

const handleFetchEmail = async (emailId: string) => {
  try {
    const token = await getAuthToken();

    const spreadsheetUpdateResponse = await fetch(
        'http://127.0.0.1:8080/company/company-job-info-crew-ai',
        {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(emailId)
        }
    );
  } catch (error: any) {
    console.error("Error fetching email summary:", error.message);
  }
};

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

const createButton = () => {
  // Create button
  const button = document.createElement('button');
  button.id = "fetch-email-summary-button";
  
  // Add spinner
  const spinner = document.createElement('span');
  spinner.style.display = 'none';
  spinner.style.width = '16px';
  spinner.style.height = '16px';
  spinner.style.border = '2px solid #ffffff';
  spinner.style.borderTopColor = 'transparent';
  spinner.style.borderRadius = '50%';
  spinner.style.animation = 'spin 0.8s linear infinite';

  // Add text container
  const textSpan = document.createElement('span');
  textSpan.textContent = 'Extract Job Details';
  
  // Add elements to button
  button.appendChild(spinner);
  button.appendChild(textSpan);

  // Style the button
  Object.assign(button.style, {
      background: 'transparent',
      color: '#4f46e5',
      border: '1px solid #4f46e5',
      padding: '6px 12px',
      marginRight: '2em',
      borderRadius: '8px',
      fontSize: '12px',
      fontWeight: '500',
      cursor: 'pointer',
      transition: 'all 0.2s',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '8px'
  });

  // Add hover effect
  button.addEventListener('mouseover', () => {
      button.style.background = '#4f46e5';
      button.style.color = 'white';
  });

  button.addEventListener('mouseout', () => {
      button.style.background = 'transparent';
      button.style.color = '#4f46e5';
  });

  // Add click handler with loading state
  button.addEventListener('click', async function(event) {
      if (button.disabled) return;
      // Store the current width before changing states
      const buttonWidth = button.offsetWidth;
      button.style.width = `${buttonWidth}px`;  

      event.stopPropagation();
      const emailId = getEmailIdFromDOM();
      if (emailId) {
        handleFetchEmail(emailId);
      } else {
        console.error("Email ID extraction failed.");
      }
      
      button.disabled = true;
      button.style.opacity = '0.7';
      button.style.cursor = 'not-allowed';
      spinner.style.display = 'inline-block';
      textSpan.style.display = 'none';
      
      // Simulate API call
      setTimeout(() => {
          button.disabled = false;
          button.style.opacity = '1';
          button.style.cursor = 'pointer';
          spinner.style.display = 'none';
          textSpan.style.display = 'inline';
          button.style.width = '';  // Reset to natural width
      }, 1500);
  });

  // Add spinner animation
  const styleSheet = document.createElement('style');
  styleSheet.textContent = `
      @keyframes spin {
          to { transform: rotate(360deg); }
      }
  `;
  return button;
}

/** Injects the "Fetch Email Summary" button after the email title */
const injectButtonWhenEmailOpened = () => {
  // Gmail usually displays the subject in an h2 with class "hP"
  const emailTitle = document.querySelector("div.gK");
  if (emailTitle) {
    if (document.getElementById("fetch-email-summary-button")) {
      return;
    }

    const button = createButton();
    emailTitle.insertBefore(button, emailTitle.firstChild);
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
