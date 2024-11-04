# test_script.py
from datetime import datetime

with open("/home/matthew/PROJECTS/project-hydra/hardcore_headless_hydra_autonomous_participate/test_cron_output.txt", "a") as f:
    f.write(f"Cron job executed at {datetime.now()}\n")