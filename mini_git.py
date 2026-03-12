import hashlib
import json
from datetime import datetime

class MiniGit:
    def __init__(self):
        self.staging = {}
        self.commits = {}
        self.branches = {"main": None}
        self.current_branch = "main"
        self.head = None

    def add(self, filename, content):
        self.staging[filename] = content
        return f"Added {filename} to staging"

    def commit(self, message):
        if not self.staging:
            return "Nothing to commit"

        commit_data = {
            "files": self.staging.copy(),
            "message": message,
            "parent": self.head,
            "timestamp": datetime.now().isoformat(),
            "branch": self.current_branch
        }

        commit_hash = hashlib.sha256(json.dumps(commit_data, sort_keys=True).encode()).hexdigest()[:8]
        self.commits[commit_hash] = commit_data
        self.head = commit_hash
        self.branches[self.current_branch] = commit_hash
        self.staging.clear()

        return f"Committed: {commit_hash} - {message}"

    def log(self):
        if not self.head:
            return "No commits yet"

        logs = []
        current = self.head
        while current:
            commit = self.commits[current]
            logs.append(f"{current}: {commit['message']} ({commit['timestamp']})")
            current = commit["parent"]

            return "\n".join(logs)

    def checkout(self, commit_hash):
        if commit_hash not in self.commits:
            return f"Commit {commit_hash} not found"

        self.head = commit_hash
        return f"Checked out to {commit_hash}"

    def branch(self, branch_name):
        if branch_name in self.branches:
            return f"Branch {branch_name} already exists"

        self.branches[branch_name] = self.head
        return f"Created branch: {branch_name}"

    def switch_branch(self, branch_name):
        if branch_name not in self.branches:
            return f"Branch {branch_name} not found"

        self.current_branch = branch_name
        self.head = self.branches[branch_name]
        return f"Switched to branch: {branch_name}"

    def get_file(self, filename):
        if not self.head:
            return None
        return self.commits[self.head]["files"].get(filename)

if __name__ == "__main__":
    print("\n=== MINI GIT ===")
    git = MiniGit()

    while True:
        print("\n" + "="*40)
        print(f"Current branch: {git.current_branch}")
        print("1. Add File")
        print("2. Commit")
        print("3. View Log")
        print("4. Create Branch")
        print("5. Switch Branch")
        print("6. Checkout Commit")
        print("7. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            filename = input("Enter filename: ")
            content = input("Enter content: ")
            print(git.add(filename, content))
        elif choice == '2':
            message = input("Enter commit message: ")
            print(git.commit(message))
        elif choice == '3':
            print("\n" + git.log())
        elif choice == '4':
            branch = input("Enter branch name: ")
            print(git.branch(branch))
        elif choice == '5':
            branch = input("Enter branch name: ")
            print(git.switch_branch(branch))
        elif choice == '6':
            commit_hash = input("Enter commit hash: ")
            print(git.checkout(commit_hash))
        elif choice == '7':
            break