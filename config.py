class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bargainbuddy:BargainBuddy@localhost:3307/bargainbuddy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '032491965ed2fb14f94a2d6084ccb218'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
