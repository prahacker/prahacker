import os
import requests

def get_latest_repos(username, token, count=4):
    url = f"https://api.github.com/users/prahacker/repos"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    repos = response.json()
    return sorted(repos, key=lambda r: r['created_at'], reverse=True)[:count]

def generate_project_card(repo):
    return f"""
        <div className="bg-gray-700 rounded-lg p-4">
          <h3 className="text-xl font-semibold mb-2">{repo['name']}</h3>
          <p className="text-sm mb-2">{repo['description'] or 'No description'}</p>
          <div className="flex justify-between items-center">
            <span className="text-xs bg-gray-600 rounded px-2 py-1">{repo['language'] or 'N/A'}</span>
            <a href="{repo['html_url']}" className="text-blue-400 hover:text-blue-300 text-sm">View Project</a>
          </div>
        </div>
    """

def update_readme(username, token):
    with open('README.md', 'r') as file:
        content = file.read()

    repos = get_latest_repos(username, token)
    project_cards = ''.join(generate_project_card(repo) for repo in repos)

    updated_content = content.replace('<!-- PROJECTS_PLACEHOLDER -->', project_cards)

    with open('README.md', 'w') as file:
        file.write(updated_content)

if __name__ == "__main__":
    github_token = os.environ['GITHUB_TOKEN']
    github_username = "yourusername"  # Replace with your GitHub username
    update_readme(github_username, github_token)
