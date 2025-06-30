# Copyright @ISmartDevs
# Channel t.me/TheSmartDev
from .gen import setup_gen_handler
from .bin import setup_bin_handler
from .info import setup_info_handler
from .fake import setup_fake_handler
from .sudo import setup_admin_handler

def setup_modules_handlers(app):
    # Register all imported handlers
    setup_gen_handler(app)
    setup_bin_handler(app)
    setup_info_handler(app)
    setup_fake_handler(app)
    setup_admin_handler(app)
