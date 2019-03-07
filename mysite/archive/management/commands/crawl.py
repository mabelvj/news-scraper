# commands/crawl.py

from django.core.management.base import BaseCommand
from nytimes.spiders.news import NewsSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())

        process.crawl(NewsSpider)
        process.start()
