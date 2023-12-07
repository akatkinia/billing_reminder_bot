FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN apt update && apt install cron -y && pip install -r requirements.txt
RUN ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime
RUN echo "0 17 11 * * /usr/local/bin/python3 /app/notify.py" | crontab
EXPOSE 443
#CMD ["python3", "bot.py"]
CMD ["bash", "-c", "(python3 bot.py &) && cron -f"]
