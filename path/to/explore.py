import os
import glob

def explore_project(base_path):
    """Explore project structure, skipping hidden and non-source directories."""
    files = []
    for root, dirs, filenames in os.walk(base_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv']]
        for f in filenames:
            if f.endswith('.py'):
                files.append(os.path.join(root, f))
    return files

# Usage
base = '/opt/axentx/surrogate-1'
backend = os.path.join(base, 'backend')

if os.path.exists(backend):
    print("Backend exists")
    print("\n".join(explore_project(backend)[:50]))
else:
    print("Backend doesn't exist at", backend)
    print("\n".join(os.listdir(base)))