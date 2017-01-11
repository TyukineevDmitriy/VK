from pyriodic import Scheduler, DurationJob
from sheduler.db_updater import DBUpdater

s = Scheduler()
db_updater = DBUpdater()

s.add_job(
    DurationJob(
        lambda: db_updater.update_db(),
        '1d'
    )
)