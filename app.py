import os
from dotenv import Dotenv
configurations = Dotenv('configurations.ini')
os.environ.update(configurations)




