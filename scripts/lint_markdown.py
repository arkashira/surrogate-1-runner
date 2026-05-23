import subprocess
import sys

def lint_markdown():
    try:
        subprocess.run(["markdownlint", "**/*.md", "--fix"], check=True)
        print("Markdown linting completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Markdown linting failed: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if lint_markdown() else 1)