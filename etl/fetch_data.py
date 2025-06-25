"""
Скачивание Breast Cancer Wisconsin Diagnostic dataset
и сохранение в CSV (raw_data.csv).

Запуск самостоятельно:
    python -m etl.fetch_data
"""
import io
import logging
import pandas as pd
import requests
from etl.config import *

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[
                        logging.FileHandler(LOGS_DIR / "fetch_data.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

COLUMN_NAMES = [
    "id", "diagnosis",
    *[f"{feat}_{stat}" for feat in [
        "radius", 'texture','perimeter', 'area', 'smoothness', 'compactness', 'concavity',
        'concave', 'symmetry', 'fractal_dimension'
    ]
      for stat in ["mean", "se", "worst"]]
]

def fetch():
    logger.info('Скачивание датасета из %s', DATA_URL)
    response = requests.get(DATA_URL, timeout=30)
    response.raise_for_status()
    logger.info('Скачивание завершено')
    return response.text

def save_csv(csv_text):
    df = pd.read_csv(
        io.StringIO(csv_text),
        header=None,
        names=COLUMN_NAMES
    )
    df.to_csv(RAW_DATA_PATH, index=False)
    logger.info("Файл сохранен")

def main():
    csv_text = fetch()
    save_csv(csv_text)

if __name__ == '__main__':
    main()
