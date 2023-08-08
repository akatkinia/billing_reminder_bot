#telegram
TOKEN_API = ''

#DB
DB_PATH = "bills.db"

# USER_IDS
ADMIN_ID = '' # для оповещения админа

# webhook settings
WEBAPP_HOST = '0.0.0.0'  # public dns/ip or 0.0.0.0


WEBAPP_PORT = 8443 # aiohttp в состсаве с aiogram работает только с 443 или 8443

# WEBHOOK_HOST = f'{WEBAPP_HOST}:{WEBAPP_PORT}' # использовать на проде
WEBHOOK_HOST = '' # для теста может использовать ngrok адрес

WEBHOOK_PATH = f'/bot{TOKEN_API}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# использовать на проде
# WEBHOOK_SSL_CERT = '/etc/letsencrypt/live/<FQDN_OF_YOUR_HOST>/fullchain.pem'  # Path to the ssl certificate
# WEBHOOK_SSL_PRIV = '/etc/letsencrypt/live/<FQDN_OF_YOUR_HOST>/privkey.pem'  # Path to the ssl private key
