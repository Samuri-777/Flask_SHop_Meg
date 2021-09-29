from os.path import join, dirname, realpath

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gop_shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'gop_shop/static/img/product/')

    # upload_folder = '/static/img/product'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
