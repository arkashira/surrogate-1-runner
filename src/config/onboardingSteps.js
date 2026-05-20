export const steps = [
  {
    id: 0,
    title: 'Welcome',
    description: 'Get started with Axentx language coach',
    content: 'This is the first step of onboarding.',
  },
  {
    id: 1,
    title: 'Features',
    description: 'Explore key features',
    content: 'Learn about the main features of the language coach.',
  },
  {
    id: 2,
    title: 'Dashboard',
    description: 'Check your progress',
    content: 'See your learning progress and upcoming activities.',
  },
  {
    id: 3,
    title: 'Preferences',
    description: 'Customize your learning',
    content: (
      <PreferencesForm />   // imported lazily inside the component
    ),
  },
];