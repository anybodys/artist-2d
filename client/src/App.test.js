import { render, screen } from '@testing-library/react';

import App from './App';


jest.mock("./api", () => {
  const VotingApi = {
    me: async function() {
      return ({});
    },

    getArt: async function () {
      return ({art: [{
        artist_id: "mock-artist-id",
        generation: "0",
        public_link: "mock-art-url"
      }]});
    }
  };
  return {VotingApi}
});

test('renders image', async () => {
  render(<App />);
  const imgElement = await screen.findByAltText(/.*mock-artist-id/);
  expect(imgElement).toBeInTheDocument();
  expect(imgElement.src).toBe('http://localhost/mock-art-url')
});
