function getUrl(path) {
  const baseUrl = process.env.REACT_APP_API_BASE_URL;
  return baseUrl + path;
}

// This one is relative to root/host.
export const LoginUri = '/accounts/google/login/';

export const VotingApi = {
  me: async function () {
    const response = await fetch(getUrl('/me'), {
      credentials: "include",
    });
    return response.json();
  },

  getArt: async function () {
    const response = await fetch(getUrl('/art'));
    return await response.json();
  },

  vote: async function (artistId) {
    await fetch(getUrl('/vote'), {
      method: 'POST',
      credentials: "include",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 'artist': artistId })
    });
  }
}
