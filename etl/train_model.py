"""
Обучение LogisticRegression и сохранение .pkl

Запуск:
    python -m etl.train_model
"""
import logging
import joblib
from sklearn.linear_model import LogisticRegression
from etl.config import *

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[
                        logging.FileHandler(LOGS_DIR / "train_model.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

def load_processed():
    return joblib.load(PROCESSED_DATA_PATH)


def train(processed):
    X_train, y_train  = processed['X_train'], processed['y_train']
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model

def save(model):
    joblib.dump(model, MODEL_PATH)
    logger.info('Модель сохранена')

def main():
    data = load_processed()
    model = train(data)
    save(model)

if __name__ == '__main__':
    main()
