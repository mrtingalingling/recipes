import { render, fireEvent } from '@testing-library/svelte';
import RecipeTabs from '../frontend/components/RecipeTabs.svelte';
import RecipeCard from '../frontend/components/RecipeCard.svelte';
import RecipeFeed from '../frontend/components/RecipeFeed.svelte';
import ExternalRecipeViewer from '../frontend/components/ExternalRecipeViewer.svelte';
import RecipeEditor from '../frontend/components/RecipeEditor.svelte';

describe('Recipe Components', () => {
  test('RecipeTabs switches tabs', async () => {
    const { getByText } = render(RecipeTabs);
    await fireEvent.click(getByText('Healthiest'));
    expect(getByText('Healthiest')).toHaveClass('active');
  });

  test('RecipeCard displays recipe', () => {
    const recipe = { title: 'Test', thumbnail: 'img.jpg', ingredients: [{ name: 'Egg', onSale: true }] };
    const { getByText } = render(RecipeCard, { recipe });
    expect(getByText('Test')).toBeTruthy();
    expect(getByText('Egg (On Sale)')).toBeTruthy();
  });

  test('RecipeFeed renders multiple cards', () => {
    const recipes = [
      { title: 'A', thumbnail: 'a.jpg', ingredients: [] },
      { title: 'B', thumbnail: 'b.jpg', ingredients: [] }
    ];
    const { getByText } = render(RecipeFeed, { recipes });
    expect(getByText('A')).toBeTruthy();
    expect(getByText('B')).toBeTruthy();
  });

  test('ExternalRecipeViewer renders iframe', () => {
    const { container } = render(ExternalRecipeViewer, { url: 'https://example.com' });
    expect(container.querySelector('iframe')).toBeTruthy();
  });

  test('RecipeEditor saves recipe', async () => {
    const { getByText } = render(RecipeEditor);
    await fireEvent.click(getByText('Save'));
    // Save event should be dispatched (mocked)
  });
});
