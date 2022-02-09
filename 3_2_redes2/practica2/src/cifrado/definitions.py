import os
from project_configuration import AUX_PATH

KEY_LENGTH = 2048
KEY_FILE = os.path.join(AUX_PATH, 'keys.pem')
AES_KEY_LENGTH = 32
IV_LENGTH = 16