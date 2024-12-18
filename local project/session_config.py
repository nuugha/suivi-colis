from dotenv import load_dotenv, set_key, find_dotenv
import os

class SessionConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionConfig, cls).__new__(cls)
            cls._instance.env_file = '.env'
            load_dotenv(cls._instance.env_file)
        return cls._instance
    
    def set(self, key, value):
        set_key(self.env_file, key, str(value))
        os.environ[key] = str(value)
    
    def get(self, key, default=None):
        return os.getenv(key, default)
    
    def clear(self):
        with open(self.env_file, 'w') as f:
            f.write('')
        os.environ.clear()
