import os

from utils.folder_file_manager import make_directory_if_not_exists


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_IMAGES_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'pdf_images'))
PDF_UPLOAD_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'static', 'upload'))
OUTPUT_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'output'))
ARCHIVE_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'archive_dir'))
INVOICE_DIR = os.path.join(CUR_DIR, 'invoice_dir')
VISION_CREDENTIAL_PATH = os.path.join(CUR_DIR, 'utils', 'credential', 'tonal-studio-295208-5eedce5679d0.json')

ROTATION_Y_THREAD = 200
Y_BIND_THREAD = 10
FRAME_THRESH_EMPHASIZE = 51
FRAME_THRESH_NOISE = 6
THREADING_ITEM = 2

LOCAL = True

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

DB_USERNAME = "root"
DB_PASSWORD = "password"
DB_NAME = "invoice_db"
DB_HOST = "localhost"
