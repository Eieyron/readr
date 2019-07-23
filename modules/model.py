import os

from modules.ai import load_models
from modules.config import num_models
 
 # suppress all logging from tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

globals()['models'] = load_models(n=num_models)