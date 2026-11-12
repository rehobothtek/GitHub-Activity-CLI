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

            print(f"- Deleted {ref_type} '{ref}' in {repo}")
    

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


