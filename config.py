import os

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = int(os.environ.get('DB_PORT'))
DB_NAME = os.environ.get('DB_NAME')
DB_USER_NAME = os.environ.get('DB_USER_NAME')
DB_USER_PASSWORD = os.environ.get('DB_USER_PASSWORD')

DB_URL = f'postgresql://{DB_USER_NAME}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
