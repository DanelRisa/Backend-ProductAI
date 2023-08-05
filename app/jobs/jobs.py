from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import scrape_arbuz, scrape_galmart, parse_both_websites

# scheduler = BackgroundScheduler()

# scheduler.add_job(scrape, "cron", hour=21, minute=30)
# # scheduler.add_job(scrape_news, "interval", hours=1)


scheduler = BackgroundScheduler()

scheduler.add_job(parse_both_websites, "cron", hour=2, minute=40)
# scheduler.add_job(scrape_galmart, "cron", hour=00, minute=55)

# scheduler.start()

# try:
#     while True:
#         pass
# except (KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()
#     client.close()

# print('Data removed and updated in MongoDB.')