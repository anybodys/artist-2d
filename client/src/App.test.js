import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders image', () => {
  render(<App />);
  const imgElement = screen.getByAltText(/.*example-artist-id-1/);
  expect(imgElement).toBeInTheDocument();
});
