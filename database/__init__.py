import os
from pymodm import connect
connect(os.getenv('mongoURL'))
