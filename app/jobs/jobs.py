from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import scrape_arbuz, scrape_galmart


# scheduler = BackgroundScheduler()

# scheduler.add_job(scrape, "cron", hour=21, minute=30)
# # scheduler.add_job(scrape_news, "interval", hours=1)


scheduler = BackgroundScheduler()

scheduler.add_job(scrape_arbuz, "cron", hour=21, minute=30)

scheduler.add_job(scrape_galmart, "cron", hour=22, minute=0)

scheduler.start()

# try:
#     while True:
#         pass
# except (KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()
#     client.close()

# print('Data removed and updated in MongoDB.')