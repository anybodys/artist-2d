function getUrl(path) {
  const baseUrl = process.env.REACT_APP_API_BASE_URL;
  return baseUrl + path;
}

export const VotingApi = {
  get: async function () {
    const response = await fetch(getUrl('/art'));
    const paintingsData = await response.json();
    return paintingsData;
  }
}
