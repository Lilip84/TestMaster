import git
import os

class GitManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            self.repo = git.Repo.init(repo_path)
        else:
            self.repo = git.Repo(repo_path)
    
    def commit_changes(self, message="Auto commit by TestMaster"):
        self.repo.git.add(A=True)
        self.repo.index.commit(message)
        return True
    
    def push_changes(self, remote_name='origin', branch='main'):
        origin = self.repo.remote(name=remote_name)
        origin.push(branch)
        return True
    
    def get_history(self, limit=10):
        commits = list(self.repo.iter_commits(max_count=limit))
        return [{
            'hexsha': c.hexsha,
            'message': c.message.strip(),
            'author': c.author.name,
            'date': c.committed_datetime.isoformat()
        } for c in commits]