from environs import Env

env = Env()
env.read_env('.env')

DEBUG = env.bool('DEBUG', default=False)


