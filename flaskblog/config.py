class Config():
    # move secure items to environment variables
    SECRET_KEY = '868335c85eb1aa9aea2aca3ddf946957'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'accounts@alualgae.com'
    MAIL_PASSWORD = '3ddf946957'
