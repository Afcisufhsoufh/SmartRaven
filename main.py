#Copyright @ISmartDevs
#Channel t.me/TheSmartDev
from utils import LOGGER
from modules import setup_modules_handlers
from core import setup_start_handler
from app import app  

setup_modules_handlers(app)
setup_start_handler(app)  

LOGGER.info("Bot Successfully Started! 💥")
app.run()