'''This maintains constants that are to be fetched from .env file and must re]main unchanged throughout the application'''
import os
from dotenv import load_dotenv

load_dotenv()

USER_FIRST_NAME = os.getenv('USER_FIRST_NAME')
USER_LAST_NAME = os.getenv('USER_LAST_NAME')
USER_FULL_NAME =  USER_FIRST_NAME + USER_LAST_NAME
USER_NAME = os.getenv('USER_NAME')
USER_MAIL_ID = os.getenv('USER_MAIL_ID')
USER_PHONE = os.getenv('USER_PHONE')

if __name__ == '__main__':
    print(USER_FIRST_NAME)
    print(USER_LAST_NAME)
    print(USER_MAIL_ID)
    print(USER_PHONE)