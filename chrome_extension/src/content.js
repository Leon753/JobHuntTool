import { getAuthToken } from "./chrome/utils";

export async function fetchEmails() {
    try {
        const token = await getAuthToken();
        const response = await fetch(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=10",
            {
                headers: { Authorization: `Bearer ${token}` },
            }
        );
        const data = await response.json();
        console.log("Emails:", data);
    } catch (error) {
        console.error("Error fetching emails:", error);
    }
  }
  