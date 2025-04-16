import logging
import os

log_path = "logs/chameleon_resume.log"

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Clear log at each run
if os.path.exists(log_path):
    open(log_path, "w").close()

# Configure logging
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)
