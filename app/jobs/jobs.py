from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import parse_both_websites


# scheduler.add_job(scrape, "cron", hour=21, minute=30)
# # scheduler.add_job(scrape_news, "interval", hours=1)


scheduler = BackgroundScheduler()

scheduler.add_job(parse_both_websites, "cron", hour=13, minute=45)

# scheduler.start()

