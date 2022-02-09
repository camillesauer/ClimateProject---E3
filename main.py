import os
from credentials import YOUR_KEY, YOUR_USERNAME
from kaggle.api.kaggle_api_extended import KaggleApi

os.environ['KAGGLE_USERNAME'] = YOUR_USERNAME
os.environ['KAGGLE_KEY'] = YOUR_KEY

api = KaggleApi()
api.authenticate()



