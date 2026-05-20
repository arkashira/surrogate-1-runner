import Shepherd from 'shepherd.js'

export const prReviewTour = new Shepherd.Tour({
  defaultStepOptions: {
    classes: 'shadow-md bg-white rounded-lg',
    scrollTo: { behavior: 'smooth', block: 'center' }
  }
})

// ... (rest of the JavaScript code for each step)