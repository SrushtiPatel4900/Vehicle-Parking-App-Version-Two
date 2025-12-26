class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///parking.db'

    # Set a valid hashing scheme (EVEN if not used)
    SECURITY_PASSWORD_HASH = 'plaintext'
    SECURITY_PASSWORD_SALT = 'dummy_salt_value'

    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
