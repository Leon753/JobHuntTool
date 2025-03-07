export async function getAuthToken() {
  return new Promise((resolve, reject) => {
      chrome.identity.getAuthToken({ interactive: true }, (token) => {
          if (chrome.runtime.lastError || !token) {
              reject(chrome.runtime.lastError);
              return;
          }
          resolve(token);
      });
  });
}
