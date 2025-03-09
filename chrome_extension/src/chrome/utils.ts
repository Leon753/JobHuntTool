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
