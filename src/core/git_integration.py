import git
import os
import logging
from typing import List, Dict, Any, Optional

class GitManager:
    """Управление Git-репозиторием для тест-кейсов"""
    
    def __init__(self, repo_path: str) -> None:
        """
        Инициализация менеджера Git
        
        :param repo_path: Путь к репозиторию
        """
        self.repo_path = repo_path
        self.logger = logging.getLogger('GitManager')
        
        # Инициализация репозитория
        if not os.path.exists(os.path.join(repo_path, '.git')):
            self.repo = git.Repo.init(repo_path)
            self.logger.info(f"Initialized new Git repository at {repo_path}")
        else:
            self.repo = git.Repo(repo_path)
            self.logger.info(f"Loaded existing Git repository at {repo_path}")
    
    def commit_changes(self, message: str = "Auto commit by TestMaster") -> bool:
        """
        Фиксирует все изменения в репозитории
        
        :param message: Сообщение коммита
        :return: Успешность операции
        """
        try:
            self.repo.git.add(A=True)
            self.repo.index.commit(message)
            self.logger.info(f"Committed changes: {message}")
            return True
        except Exception as e:
            self.logger.error(f"Commit failed: {str(e)}")
            return False
    
    def push_changes(self, remote_name: str = 'origin', branch: str = 'main') -> bool:
        """
        Отправляет изменения в удаленный репозиторий
        
        :param remote_name: Имя удаленного репозитория
        :param branch: Ветка для отправки
        :return: Успешность операции
        """
        try:
            origin = self.repo.remote(name=remote_name)
            push_result = origin.push(branch)
            
            # Проверка успешности операции
            if push_result[0].flags & push_result[0].ERROR:
                self.logger.error(f"Push failed: {push_result[0].summary}")
                return False
            
            self.logger.info(f"Pushed changes to {remote_name}/{branch}")
            return True
        except Exception as e:
            self.logger.exception(f"Push error: {str(e)}")
            return False
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Возвращает историю коммитов
        
        :param limit: Максимальное количество коммитов
        :return: Список коммитов
        """
        try:
            commits = list(self.repo.iter_commits(max_count=limit))
            return [{
                "hexsha": c.hexsha,
                "message": c.message.strip(),
                "author": c.author.name,
                "date": c.committed_datetime.isoformat()
            } for c in commits]
        except Exception as e:
            self.logger.error(f"Failed to get history: {str(e)}")
            return []