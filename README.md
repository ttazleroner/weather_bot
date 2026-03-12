# weather_bot
Telegram weather bot on aiogram 3 + aiohttp (OpenWeather), async, python



1) What it can do
Get city weather via OpenWeather
UX: button → city input → response (FSM 1 state)
Store users/activity in PostgreSQL (raw SQL)
FSM storage in Redis (Docker)

3) Stack
Python 3.11
aiogram 3.x
aiohttp
PostgreSQL (Docker)
Redis (Docker)
psycopg 3 async + pool

4) Quick start (the most important)
Example:

# 1) raise the infrastructure
docker compose up -d

# 2) configure environment variables
copy .env.example .env
# (and fill in .env by hand)

# 3) create tables
python -m migrations.create_table

# 4) start the bot
python main.py
4) Environment variables
A list of what needs to be filled in .env (without real values), for example:

BOT_TOKEN
API_KEY
DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
REDIS_HOST, REDIS_PORT, REDIS_DB (if any)
5) Project structure (briefly)
handlers/ — handlers
services/ — working with API
infrastructure/ — DB/pool/queries
migrations/ — creating tables
