"""
Оценка модели: Accuracy, Precision, Recall, F1
и запись metrics.json.

Запуск:
    python -m etl.evaluate
"""
import json
import logging
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from etl.config import *

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[
                        logging.FileHandler(LOGS_DIR / "evaluate.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

def load():
    processed = joblib.load(PROCESSED_DATA_PATH)
    model = joblib.load(MODEL_PATH)
    return processed, model

def calculate_metrics(processed, model):
    X_test, y_test = processed['X_test'], processed['y_test']
    y_pred = model.predict(X_test)
    metrics = {
        'accuracy' : accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred)
    }
    return  metrics

def save(metrics):
    with open(METRICS_PATH, "w", encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    logger.info("Метрики сохранены")

def main():
    processed, model = load()
    metrics = calculate_metrics(processed,model)
    save(metrics)
    logger.info("Метрики: %s", metrics)

if __name__ == '__main__':
    main()

