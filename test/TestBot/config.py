from environs import Env

env = Env()
env.read_env()

API_BOT = env.str("API_BOT")