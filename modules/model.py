import os

from modules.ai import load_models
from modules.config import num_models

globals()['models'] = load_models(n=num_models)