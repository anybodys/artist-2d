function getUrl(path) {
  const baseUrl = process.env.REACT_APP_API_BASE_URL;
  return baseUrl + path;
}

export const LoginUri = getUrl('/accounts/google/login/');

export const VotingApi = {
  me: async function() {
    const response = await fetch(getUrl('/me'), {
      credentials: "include",
    });
    return response.json();
  },

  getArt: async function () {
    const response = await fetch(getUrl('/art'));
    return await response.json();
  }
}
