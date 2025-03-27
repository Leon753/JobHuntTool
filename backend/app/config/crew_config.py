
import os 
import yaml

current_dir = os.path.dirname(os.path.abspath(__file__))
# Load YAML Configuration
def load_config(file:str):
    config_path = os.path.join(current_dir, file)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    with open(config_path,"r") as file:
        return yaml.safe_load(file)

agents_config = load_config("agents.yaml")
tasks_config = load_config("tasks.yaml")
