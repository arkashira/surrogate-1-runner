
import { createGuidedTour, startGuidedTour } from './guided_tour';

describe('Guided Tour Module', () => {
  beforeEach(() => {
    jest.spyOn(console, 'log').mockImplementation(() => {});
    jest.spyOn(console, 'warn').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('startGuidedTour logs all steps and marks completion', () => {
    const tour = createGuidedTour({
      steps: [
        {
          id: 'welcome',
          title: 'Welcome to Axentx',
          description: 'Let’s walk through the main features of the platform.',
          element: null,
        },
        // Add more steps as needed
      ],
      persistState: true,
    });

    const onStepMock = jest.fn();

    startGuidedTour(tour);

    expect(onStepMock).toHaveBeenCalledTimes(6);
    expect(console.log).toHaveBeenCalledWith(
      expect.stringContaining('Step 1/6: Welcome to Axentx')
    );
    expect(tour.isTourCompleted()).toBe(true);
  });

  test('startGuidedTour does nothing if already completed', () => {
    localStorage.setItem('guidedTourCompleted', 'true');

    const tour = createGuidedTour({ persistState: true });

    startGuidedTour(tour);

    expect(console.warn).toHaveBeenCalledWith(
      'Guided tour has already been completed.'
    );
    expect(console.log).not.toHaveBeenCalled();
  });

  test('resetTour clears completion flag', () => {
    localStorage.setItem('guidedTourCompleted', 'true');
    const tour = createGuidedTour({ persistState: true });
    tour.resetTour();
    expect(tour.isTourCompleted()).toBe(false);
  });
});