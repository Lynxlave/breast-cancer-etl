"""
Загрузка артефактов в Cloud.ru Object Storage (S3-совместимый API)
или сохранение локально, если USE_CLOUD=false.
"""
import logging
import boto3
from botocore.config import Config
from etl.config import *

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[
                        logging.FileHandler(LOGS_DIR / "upload.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

def upload(local_path, key, client):
    logger.info("Приступили к загрузке файлов")
    client.upload_file(str(local_path), CLOUD_BUCKET, key)

def main():
    if not USE_CLOUD:
        logger.info("Отправление в облачное хранилище отключено, файлы остаются локально в %s", ARTIFACTS_DIR)
        return
    try:
        s3_config = Config(
            region_name = 'ru-central-1'
        )
        client = boto3.client(
            's3',
            endpoint_url = CLOUD_ENDPOINT,
            aws_access_key_id=f"{CLOUD_TENANT_ID}:{CLOUD_ACCESS_KEY}",
            aws_secret_access_key = CLOUD_SECRET_KEY,
            config=s3_config
        )
        upload(MODEL_PATH, f"{CLOUD_PREFIX}{MODEL_PATH.name}", client)
        upload(METRICS_PATH, f"{CLOUD_PREFIX}{METRICS_PATH.name}", client)

        logger.info('Загрузка файлов завершена')
    except Exception as e:
        logger.error("При загрузке в Cloud.ru произошла ошибка: %s", e)

if __name__ == '__main__':
    main()

