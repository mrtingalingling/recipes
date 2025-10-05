import { render, fireEvent } from '@testing-library/svelte';
import DealsView from '../frontend/components/DealsView.svelte';

describe('DealsView', () => {
  test('renders map and list views', async () => {
    const { getByText, container } = render(DealsView);
    expect(getByText('Map View')).toBeTruthy();
    expect(getByText('List View')).toBeTruthy();
    // Switch to list view
    await fireEvent.click(getByText('List View'));
    expect(container.querySelector('ul')).toBeTruthy();
    // Switch to map view
    await fireEvent.click(getByText('Map View'));
    expect(container.querySelector('#map')).toBeTruthy();
  });
});
