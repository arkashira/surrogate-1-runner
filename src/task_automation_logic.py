import github3
from typing import List, Dict, Optional
import logging
import os

class GitHubTaskAutomation:
    def __init__(self, github_token: str):
        self.github = github3.login(token=github_token)
        self.connected_repos = []
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def connect_repository(self, repo_full_name: str) -> bool:
        """Connect to a GitHub repository and store it for task automation"""
        try:
            repo = self.github.repository_from_full_name(repo_full_name)
            if repo is None:
                self.logger.error(f"Repository {repo_full_name} not found")
                return False
                
            self.connected_repos.append({
                'full_name': repo_full_name,
                'owner': repo.owner.login,
                'name': repo.name,
                'default_branch': repo.default_branch
            })
            self.logger.info(f"Successfully connected to {repo_full_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error connecting to repository: {str(e)}")
            return False

    def list_connected_repos(self) -> List[Dict]:
        """Return list of connected repositories with metadata"""
        return self.connected_repos

    def execute_automation_task(self, task_type: str, repo_full_name: str, **kwargs) -> Dict:
        """Execute automation task on specified repository"""
        try:
            repo = self.github.repository_from_full_name(repo_full_name)
            if repo is None:
                return {"success": False, "error": "Repository not found"}
                
            if task_type == "auto_merge_pr":
                pr_number = kwargs.get('pr_number')
                pr = repo.pull_request(pr_number)
                if pr.is_mergeable():
                    pr.merge()
                    return {"success": True, "message": f"PR #{pr_number} merged successfully"}
                return {"success": False, "error": "PR not mergeable"}
                
            elif task_type == "create_issue":
                title = kwargs.get('title')
                body = kwargs.get('body')
                repo.create_issue(title, body)
                return {"success": True, "message": f"Issue created with title: {title}"}
                
            else:
                return {"success": False, "error": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            self.logger.error(f"Task execution failed: {str(e)}")
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Example usage for testing
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
        
    automation = GitHubTaskAutomation(github_token)
    
    # Connect test repository
    automation.connect_repository("octocat/Hello-World")
    
    # List connected repositories
    print("Connected Repositories:")
    for repo in automation.list_connected_repos():
        print(f"- {repo['full_name']} (default branch: {repo['default_branch']})")
        
    # Example task execution
    result = automation.execute_automation_task(
        "auto_merge_pr",
        "octocat/Hello-World",
        pr_number=123
    )
    print("\nTask Result:", result)