import sys
import urllib.request
import json
from urllib.error import HTTPError, URLError


def fetch_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        return data

    except HTTPError as error:
        if error.code == 404:
            print("Error: GitHub username not found.")
        elif error.code == 403:
            print("Error: GitHub API rate limit exceeded.")
        else:
            print(f"HTTP Error: {error.code}")

        return None

    except URLError:
        print("Error: Unable to connect to GitHub. Check your internet connection.")
        return None

def display_activity(activity):
    if not activity:
        print("No recent public activity found.")
        return
    
    print(f"\nFound {len(activity)} recent activities:\n")
        
    for event in activity:
        event_type = event.get("type")
        repo = event.get("repo", {}).get("name")

        if event_type == "PushEvent":
            commits = event.get("payload", {}).get("commits", [])

            if commits:
                print(f"- Pushed {len(commits)} commits to {repo}")
            else:
                print(f"- Pushed changes to {repo}")

        elif event_type == "WatchEvent":
            print(f"- Starred {repo}")

        elif event_type == "CreateEvent":
            payload = event.get("payload", {})
            ref = payload.get("ref")
            ref_type = payload.get("ref_type")

            if ref:
                print(f"- Created {ref_type} '{ref}' in {repo}")
            else:
                print(f"- Created a new repository: {repo}")

        elif event_type == "DeleteEvent":
            payload = event.get("payload", {})
            ref = payload.get("ref")
            ref_type = payload.get("ref_type")

            if ref and ref_type:
                print(f"- Deleted {ref_type} '{ref}' in {repo}")
            else:
                print(f"- Deleted something in {repo}")
                    
        elif event_type == "ForkEvent":
            payload = event.get("payload", {})
            forked_repo = payload.get("forkee", {}).get("full_name")

            if forked_repo:
                print(f"- Forked {repo} into {forked_repo}")
            else:
                print(f"- Forked {repo}")
        
        elif event_type == "IssuesEvent":
            payload = event.get("payload", {})
            action = payload.get("action")
            issue = payload.get("issue", {})
            title = issue.get("title") 
            
            if action and title:
                print(f"- {action.capitalize()} issue '{title}' in {repo}")
            else:
                print(f"- issue activity in {repo}")
                
        elif event_type == "PullRequestEvent":
            payload = event.get("payload", {})
            action = payload.get("action")
            pull_request = payload.get("pull_request", {})
            title = pull_request.get("title")
            
            if action and title:
                print(f"- {action.capitalize()} pull request '{title}' in {repo}")
            else:
                print(f"- Pull request activity in {repo}")
                
        elif event_type == "ReleaseEvent":
            payload = event.get("payload", {})
            action = payload.get("action")
            release = payload.get("release", {})
            name = release.get("name") or release.get("tag_name")
            
            if action and name:
                print(f"- {action.capitalize()} release '{name}' in {repo}")
            else:
                print(f"- Release activity in {repo}")
        
        elif event_type == "PublicEvent":
            print(f"- Made repository {repo} public")
                
def main():
    if len(sys.argv) < 2:
        print("usage: python main.py <username>")
        return

    username = sys.argv[1]

    print(f"Fetching Github Activity for: {username}")

    activity = fetch_activity(username)

    if activity is not None:
        display_activity(activity)


if __name__ == "__main__":
    main()


