import os
import requests
from typing import Dict, List, Optional

def get_repo_languages(username: str, repo: str, token: str) -> Dict[str, int]:
    url = f"https://api.github.com/repos/{username}/{repo}/languages"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def calculate_primary_language(languages: Dict[str, int]) -> Optional[str]:
    if not languages:
        return None
    return max(languages.items(), key=lambda x: x[1])[0]

def get_latest_repos(username: str, token: str, count: int = 4) -> List[Dict]:
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    repos = response.json()
    
    sorted_repos = sorted(repos, key=lambda r: r['created_at'], reverse=True)[:count]
    
    for repo in sorted_repos:
        languages = get_repo_languages(username, repo['name'], token)
        repo['primary_language'] = calculate_primary_language(languages)
        
    return sorted_repos

def generate_project_card(repo: Dict) -> str:
    # Using markdown table format for better visual organization
    return f"""
### [{repo['name']}]({repo['html_url']})
{repo['description'] or 'No description provided.'}

![Language](https://img.shields.io/badge/{repo['primary_language'] or 'N/A'}-{repo['language'] or 'gray'}-blue?style=flat-square)
![Stars](https://img.shields.io/github/stars/{repo['full_name']}?style=flat-square)
"""

def update_readme(username: str, token: str):
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()

    repos = get_latest_repos(username, token)
    project_cards = '\n'.join(generate_project_card(repo) for repo in repos)
    
    # Find the position between the Latest Projects heading and the next section
    start_marker = "🚀 Latest Projects"
    end_marker = "📊 GitHub Stats"
    
    # Split content and replace the projects section
    parts = content.split(start_marker)
    if len(parts) > 1:
        rest = parts[1].split(end_marker)
        updated_content = (
            parts[0] + 
            start_marker + '\n\n' + 
            project_cards + '\n\n' + 
            end_marker +
            rest[1]
        )
        
        with open('README.md', 'w', encoding='utf-8') as file:
            file.write(updated_content)

if __name__ == "__main__":
    github_token = os.environ['GITHUB_TOKEN']
    github_username = "prahacker"  # Your GitHub username
    update_readme(github_username, github_token)
