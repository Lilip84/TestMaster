import os
import json
from typing import Dict, Any

class ConfigDB:
    CONFIG_FILE = "connections.json"
    
    @classmethod
    def load_connections(cls) -> Dict[str, Any]:
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {
            "web_base_url": "",
            "api_base_url": "",
            "db_url": ""
        }
    
    @classmethod
    def save_connections(cls, config: Dict[str, Any]) -> None:
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    
    @classmethod
    def get_connection(cls, key: str, default: str = "") -> str:
        config = cls.load_connections()
        return config.get(key, default)