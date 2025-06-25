"""
Предобработка: очистка, масштабирование, train/test split,
сериализация в Parquet.

Запуск:
    python -m etl.preprocess
"""

import logging
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from etl.config import *

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[
                        logging.FileHandler(LOGS_DIR / "preprocess.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

def load_row():
    return pd.read_csv(RAW_DATA_PATH)

def preprocess(df):
    logger.info("Начата обработка данных")
    df = df.drop(columns=['id'])
    df["diagnosis"] = df["diagnosis"].map({"M" : 1, "B" : 0})

    X = df.drop(columns = ['diagnosis'])
    y = df['diagnosis']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

    processed = {
        "X_train" : X_train,
        "X_test": X_test,
        "y_train" : y_train,
        "y_test": y_test,
        "scaler" : scaler
    }
    return processed

def save(processed, path = PROCESSED_DATA_PATH):
    logger.info("Сохранение обработанных данных")
    joblib.dump(processed, path)

def main():
    df = load_row()
    processed = preprocess(df)
    save(processed)

if __name__ == '__main__':
    main()