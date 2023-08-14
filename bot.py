import ssl
from aiogram.utils.executor import start_webhook

from create_bot import dp, on_startup, on_shutdown
from handlers import common
from config import WEBAPP_HOST, WEBHOOK_PATH, WEBAPP_PORT, WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV


if __name__ == '__main__':
    common.register_handlers_common(dp)

    # Generate SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        ssl_context=context
    )
