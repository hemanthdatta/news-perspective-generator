from pathlib import Path
import yaml
from typing import Dict, Any,Union
import os,sys

def read_yaml_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    yaml_path = Path(file_path)
    if not yaml_path.exists():
        raise FileNotFoundError(f"{yaml_path} not found")
    
    try:
        with open(yaml_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config
    except UnicodeDecodeError as e:
        print(f"Encoding error: Please ensure the file is saved with UTF-8 encoding. Error: {e}")
        raise
    except yaml.YAMLError as e:
        print(f"YAML parsing error: Please check your YAML syntax. Error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error reading YAML file: {e}")
        raise