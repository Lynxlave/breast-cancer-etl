import os
from pathlib import Path
from  dotenv import load_dotenv
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_URL = os.getenv('DATA_URL')
ARTIFACTS_DIR = PROJECT_ROOT / os.getenv('ARTIFACTS_DIR')
ARTIFACTS_DIR.mkdir(exist_ok=True)
LOGS_DIR = PROJECT_ROOT / os.getenv('LOGS_DIR')
LOGS_DIR.mkdir(exist_ok=True)

RAW_DATA_PATH = ARTIFACTS_DIR / 'raw_data.csv'
PROCESSED_DATA_PATH = ARTIFACTS_DIR / 'processed.parquet'
MODEL_PATH = ARTIFACTS_DIR / 'model.pkl'
METRICS_PATH = ARTIFACTS_DIR / 'metrics.json'

USE_CLOUD=os.getenv('USE_CLOUD', "false").lower() == "true"
CLOUD_ENDPOINT=os.getenv('CLOUD_ENDPOINT', 'https://s3.cloud.ru')
CLOUD_ACCESS_KEY=os.getenv('CLOUD_ACCESS_KEY')     # Key ID
CLOUD_SECRET_KEY=os.getenv('CLOUD_SECRET_KEY')    # Secret
CLOUD_TENANT_ID=os.getenv("CLOUD_TENANT_ID")
CLOUD_BUCKET=os.getenv('CLOUD_BUCKET')
CLOUD_PREFIX=os.getenv('CLOUD_PREFIX', "")

RANDOM_STATE = 42
TEST_SIZE = 0.2