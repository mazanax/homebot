# Homebot

Dummyhome Telegram bot.

## Functions:
1. Download youtube videos

## How to use

```yaml
version: "3"
services:
  redis:
    image: redis:latest
    restart: always
    volumes:
      - ./redis:/data
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
  bot:
    image: mazanax/homebot:latest
    container_name: bot
    env_file: .env
    restart: always      
    entrypoint: ["python", "main.py"]
  worker:
    image: mazanax/homebot:latest
    container_name: worker
    env_file: .env
    restart: always
    volumes: 
      - /downloads:/app/downloads
    entrypoint: ["celery", "-A", "tasks", "worker", "--loglevel=INFO"]
```