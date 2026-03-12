from dataclasses import dataclass
from environs import Env

@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int

@dataclass
class TgBot:
    token: str

@dataclass
class LogSettings:
    level: str
    format: str

@dataclass
class RedisConfig:
    host: str
    port: int
    password: str
    db_number: int

@dataclass
class WeatherAPI:
    api: str

@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis: RedisConfig
    api: WeatherAPI
    log: LogSettings

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    
    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN")
        ),
        db = DbConfig(
            host = env.str ("DB_HOST"),
            password = env.str ("DB_PASSWORD"),
            user = env.str ("DB_USER"),
            database = env.str ("DB_NAME"),
            port = env.int ("DB_PORT")
        ),
        redis = RedisConfig(
            host= env.str("REDIS_HOST"),
            port= env.int("REDIS_PORT"),
            password=env.str("REDIS_PASSWORD"),
            db_number=env.int('REDIS_DATABASE', 2)
        ),
        api = WeatherAPI(
            api=env.str('API_KEY')
        ),
        log=LogSettings(
            level=env('LOG_LEVEL', 'INFO'),
            format=env('LOG_FORMAT', '%(asctime)s - %(name)s - %(message)s')
    )
    )