import json
import os
import sys

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

def export_openapi():
    schema = app.openapi()
    print(json.dumps(schema, indent=2))

if __name__ == "__main__":
    export_openapi()
