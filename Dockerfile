FROM python:slim
WORKDIR /app
COPY . .
RUN apt update && apt install cron -y && pip install -r requirements.txt
RUN ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime
RUN crontab /app/cron.config
EXPOSE 443
CMD ["bash", "-c", "(python3 bot.py &) && cron -f"]
