import { useState } from "react";

import { getAuthToken } from "../chrome/utils";
import { parseEmailParts } from "../helpers/helperFn";
import CircularProgress from '@mui/material/CircularProgress';
import { Button } from "@mui/material";


interface Props {}

type Email = {
  id: string
}

function MainFrame() {
  const [emailSummaryData, setEmailSummaryData] = useState<String[]>([]);
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
        const emailDetails = parseEmailParts(emailData.payload.parts);
        console.log(emailDetails);


        const emailSummaryResponse = await fetch(
          'http://127.0.0.1:8080/company/email-summary',
          {
            method: "POST",
            headers: {
             "Content-Type": 'application/json'
            },
            body: JSON.stringify({
              content: emailDetails.join(" ")
            })
          }
        );
        const emailSummary = await emailSummaryResponse.json();
        console.log("Email Summary:");
        console.log(emailSummary);
        setEmailSummaryData(emailSummary.data.content);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div>Hello. Let's start by fetching your emails</div>
      <Button onClick={fetchEmails}>Fetch Emails</Button>
      <>
      {
        loading ? 
        <CircularProgress /> : <>{emailSummaryData}</>
      }</>
    </>
  );
}

export default MainFrame;
