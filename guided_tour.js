
class GuidedTour {
  constructor(options) {
    this.steps = options.steps || [];
    this.currentStep = 0;
    this.callbacks = options.callbacks || {};
    this.persistState = options.persistState || false;
    this.storageKey = options.storageKey || 'guidedTourCompleted';
  }

  start() {
    if (this.isTourCompleted()) {
      console.warn('Guided tour has already been completed.');
      return;
    }

    this.showStep();
  }

  showStep() {
    const step = this.steps[this.currentStep];
    if (!step) return;

    const target = document.querySelector(step.element || step.target);
    if (!target) return;

    const tooltip = document.createElement('div');
    tooltip.innerHTML = `
      <div class="tooltip-content">
        ${step.title}<br>
        ${step.description}
        <button class="next-btn">Next</button>
      </div>
    `;
    tooltip.classList.add('tooltip');
    target.appendChild(tooltip);

    const nextBtn = tooltip.querySelector('.next-btn');
    nextBtn.addEventListener('click', () => {
      this.nextStep();
    });

    if (this.persistState) {
      localStorage.setItem(this.storageKey, 'true');
    }

    this.callbacks.onStep && this.callbacks.onStep(step);
  }

  nextStep() {
    this.currentStep++;
    this.showStep();
  }

  isTourCompleted() {
    return this.persistState ? localStorage.getItem(this.storageKey) === 'true' : false;
  }

  resetTour() {
    localStorage.removeItem(this.storageKey);
  }
}

export function createGuidedTour(options) {
  return new GuidedTour(options);
}

export function startGuidedTour(tour) {
  tour.start();
}