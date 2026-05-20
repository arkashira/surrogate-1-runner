const templates = [
  {
    id: 'blog-outline-generator',
    name: 'Blog Outline Generator',
    description: 'Generates a basic outline for a blog post.',
    model: 'axentx/blog-outline-model',
    prompt: 'Generate a blog outline about {{topic}}',
  },
  {
    id: 'social-media-scheduler',
    name: 'Social Media Scheduler',
    description: 'Schedules social media posts for the next week.',
    model: 'axentx/social-media-model',
    prompt: 'Schedule social media posts for the next week about {{topic}}',
  },
  // Add more templates as needed
];

export default templates;