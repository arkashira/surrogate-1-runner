"""
Defines the onboarding steps.
Each step is a dict that can contain:
  - id: int
  - title: str
  - content: str
  - video: str | None
  - interactive: str | None  (key into INTERACTIVE_RENDERERS)
"""

ONBOARDING_STEPS = [
    {
        "id": 1,
        "title": "Welcome to Axentx",
        "content": "Get started with a quick overview of the platform.",
        "video": None,
        "interactive": None,
    },
    {
        "id": 2,
        "title": "Create Your First Project",
        "content": "Learn how to create and configure a new project.",
        "video": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "interactive": None,
    },
    {
        "id": 3,
        "title": "Explore Features",
        "content": "Dive into the core features of the platform.",
        "video": None,
        "interactive": "feature_quiz",
    },
    {
        "id": 4,
        "title": "Get Support",
        "content": "Find help resources and community forums.",
        "video": None,
        "interactive": None,
    },
]