from environs import Env

env = Env()
env.read_env('.env')

DEBUG = env.bool('DEBUG', default=False)

OANDA_DOMAIN = env.str('OANDA_DOMAIN', 'DEMO')
OANDA_ACCESS_TOKEN = env.str('OANDA_ACCESS_TOKEN', '')
OANDA_ACCOUNT_ID = env.str('OANDA_ACCOUNT_ID', '')
OANDA_APPLICATION_NAME = env.str('OANDA_APPLICATION_NAME', 'TestApp')

FXCM_ACCESS_TOKEN = env.str('FXCM_ACCESS_TOKEN', '')
FXCM_ACCOUNT_ID = env.str('FXCM_ACCOUNT_ID', '')

