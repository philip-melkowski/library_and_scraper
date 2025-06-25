import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'


    def __init__(self, month='1', year='2025', **kwargs):
        super().__init__(**kwargs)
        self.page = 1
        self.month = month
        self.year = year
        self.start_urls=[f'https://lubimyczytac.pl/top100?page=1&listId=listTop100&month={self.month}&year={self.year}&paginatorType=Standard']



    def parse(self, response):
        for books in response.css('div.authorAllBooks__singleCenter'):
            full_author = books.css('div.authorAllBooks__singleTextAuthor a::text').get()
            if(full_author):
                parts = full_author.strip().split()
                nazwisko = parts[-1]
                imie = " ".join(parts[:-1])
            yield {
                'tytul': books.css('a.authorAllBooks__singleTextTitle::text').get().replace('\n', '').strip(" ")
                , 'autorImie': imie
                , 'autorNazwisko' : nazwisko

            }
        next_page = response.css('a.page-link.stdPaginator.btn')
        if next_page is not None:
            self.page +=1
            new_url = f'https://lubimyczytac.pl/top100?page={self.page}&listId=listTop100&month={self.month}&year={self.year}&paginatorType=Standard'
            yield response.follow(new_url, callback=self.parse)


