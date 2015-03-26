import rvd
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

rvd.app.run(
    host=rvd.app.config["FRONTEND_HOST_IP"],
    port=rvd.app.config["FRONTEND_PORT"]
)