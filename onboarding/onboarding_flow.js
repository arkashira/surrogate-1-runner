/**
 * Onboarding flow definition.
 *
 * Each step is an object with:
 *   - id: unique identifier
 *   - title: display title
 *   - component: relative path to the HTML component
 *
 * The onboarding renderer consumes this array to build the wizard.
 */
module.exports = [
  {
    id: 'welcome',
    title: 'Welcome',
    component: 'welcome.html',
  },
  {
    id: 'profile',
    title: 'Profile Setup',
    component: 'profile.html',
  },
  {
    id: 'content_marketing_guide',
    title: 'Content Marketing Guide',
    component: 'content_marketing_guide.html',
  },
];