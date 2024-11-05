import os
import requests
from typing import Dict, List, Optional
from datetime import datetime

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
    # Get the language color (default to blue for unknown languages)
    lang_colors = {
        "Python": "3776AB",
        "TypeScript": "3178C6",
        "JavaScript": "F7DF1E",
        "HTML": "E34F26",
        "CSS": "1572B6"
    }
    lang = repo['primary_language'] or "Unknown"
    color = lang_colors.get(lang, "0366D6")
    
    return f"""<div align="center">

[![{repo['name']}](https://img.shields.io/badge/{repo['name']}-black?style=for-the-badge&logo=github)](https://github.com/{repo['full_name']}) [![Language](https://img.shields.io/badge/{lang}-{color}?style=for-the-badge&logo={lang.lower()}&logoColor=white)](https://github.com/{repo['full_name']})

</div>"""

def update_readme(username: str, token: str):
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()

    repos = get_latest_repos(username, token)
    project_cards = '\n'.join(generate_project_card(repo) for repo in repos)
    
    # Find the position between the Latest Projects heading and the next section
    start_marker = "🚀 Latest Projects"
    end_marker = "📊 GitHub Stats"
    
    if start_marker in content:
        parts = content.split(start_marker)
        if end_marker in parts[1]:  # Check if end_marker exists after start_marker
            rest = parts[1].split(end_marker)
            updated_content = (
                parts[0] +
                start_marker + '\n\n' +
                project_cards + '\n\n' +
                end_marker +
                rest[1]
            )
        else:
            # If end_marker is missing, add project cards at the end of the start_marker section
            updated_content = (
                parts[0] +
                start_marker + '\n\n' +
                project_cards + '\n\n'
            )
    else:
        # If start_marker is missing, append projects at the end of the file
        updated_content = content + '\n\n' + start_marker + '\n\n' + project_cards

    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == "__main__":
    token = os.environ['TOKEN']
    github_username = "prahacker"  # Your GitHub username
    update_readme(github_username, token)
