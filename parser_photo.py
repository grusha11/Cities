from icrawler.builtin import GoogleImageCrawler

google_crawler = GoogleImageCrawler(storage={'root_dir': 'C:/Users/www/PycharmProjects/pythonProject1/my_projects/photos'})

google_crawler.crawl(keyword='Владимир', max_num=1)