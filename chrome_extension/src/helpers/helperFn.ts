
import type { EmailPart } from "./types";

export function decodeBase64UrlSafe(base64String: String) {
    // Convert URL-safe Base64 to standard Base64
    let base64 = base64String.replace(/-/g, "+").replace(/_/g, "/");
  
    // Decode Base64 string
    let decodedString = atob(base64);
  
    // Return readable text
    return decodeURIComponent(escape(decodedString));
  }

  export function parseEmailParts(emailParts: EmailPart[]) {
    const result: String[] = []
    for (const part of emailParts) {
        var humanReadableString = decodeBase64UrlSafe(part.body.data);
        result.push(humanReadableString);
    }
    return result;
  }
  