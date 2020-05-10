import os

class Config(object):
    SECRET_KEY = os.environ.get('AWD_PROJECT_KEY') or 'dlaskjaskld3290432LKNlk4094'