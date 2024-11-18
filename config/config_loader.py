import yaml
import os


class ConfigLoader:
    def __init__(self, config_path="config/config.yml"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from YAML file"""
        try:
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"Config file not found: {self.config_path}")

            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Error loading config: {str(e)}")
