// src/chrome/utils.ts
export async function getAuthToken(): Promise<string> {
  const tryGetToken = (): Promise<string> => {
    return new Promise((resolve, reject) => {
      chrome.runtime.sendMessage({ action: "getAuthToken" }, (response: any) => {
        if (response && response.token) {
          resolve(response.token);
        } else {
          reject(response && response.error);
        }
      });
    });
  };

  try {
    return await tryGetToken();
  } catch (error) {
    console.error("Error getting auth token, retrying:", error);
    // Wait 1 second before retrying
    await new Promise((res) => setTimeout(res, 1000));
    return tryGetToken();
  }
}

export async function getUserEmail(): Promise<string> {
  try {
    const token = await getAuthToken();
    const response = await fetch("https://www.googleapis.com/oauth2/v2/userinfo", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch user info: ${response.statusText}`);
    }

    const data = await response.json();
    return data.email; // The email address of the authenticated user
  } catch (error) {
    console.error("Error fetching user email:", error);
    throw error;
  }
}
