from marketSpiders.spiders import vierci, salemma, real
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

def main():
   settings_file_path = 'marketSpiders.settings' #settings path from this py file 
   os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
   process = CrawlerProcess(get_project_settings())
   process.crawl(vierci.superseisSpider)
   process.crawl(vierci.stockSpider)
   process.crawl(real.realSpider)
   process.crawl(salemma.SalemmaSpider)
   process.start()
   get_project_settings()

if __name__ == '__main__':
   main()
