import scrapy
import pandas as pd
from scrapy_selenium import SeleniumRequest
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://www.surplex.com/en/s.html?page=1&search={}'

class PlexSpider(scrapy.Spider):
    name = 'plex'
    def start_requests(self):
        for index in df:
            yield scrapy.Request(url=base_url.format(index), meta={"pyppeteer": True}, callback=self.parse, cb_kwargs={'index':index})

    def parse(self, response, index):
        total_pages = response.xpath("//div[@class='dropdown-menu dropdown-menu-right']/span[last()]/text()").get()             
        current_page =response.xpath("//div[@class='dropdown-menu dropdown-menu-right']/span[@class='dropdown-item js-link active']/text()").get()  
        url = response.url   
        if total_pages and current_page:
            page1 = total_pages.split('page ')
            page2 = page1[1]
            page3 = page2.split('/')
            total = page3[1]
           
            current1 = current_page.split('page ')
            current2 = current1[1]
            current3 = current2.split('/')  
            current = current3[0]
            
            if int(current) ==1:
                for i in range(2, int(total)+1): 
                    min = 'page='+str(i-1)
                    max = 'page='+str(i)
                    url = url.replace(min,max)                                                                  
                    yield response.follow(url, cb_kwargs={'index':index})

        links = response.css(".kachel--boxL a::attr(href)")   
        for link in links:            
            yield response.follow("https://www.surplex.com"+link.get(), callback=self.parse_item, cb_kwargs={'index':index})  

    def parse_item(self, response, index): 
        print(".................")          
        product_url = response.url
        print(product_url)   
        image = response.xpath('//*[@id="imageGallery-slide01"]/img/@src').get()     
        print(image)   
        auction_date = ''  
               
        try:
            auction = response.css('div.bidbox-enddate::text').get()
            auction_date = auction.strip()
            print(auction_date)
        except:
            auction_date = ''    
        loc = response.xpath("//span[@class='link-map machine--location']/span/text()").get() 
        location = loc.strip()      
        print(location)
        name = response.xpath("//div[@class='page--headline machine--pageHead']/h1/text()[2]").get()
        product_name = name.strip()
        print(product_name)
        lot = response.xpath("//div[@class='page--headline machine--pageHead']/h1/span/text()[2]").get()
        lot_number = lot[13:]
        print(lot_number)
        auctioner = response.xpath("//div[@class='page--headline machine--pageHead']/h1/span/a/text()").get()
        print(auctioner)
        description = response.xpath("//table[@class='table table-inAccordion js-machine-description']//td/text()").get()
        print(description)
        
        yield{
            
            'product_url' : response.url,           
            'item_type' :index.strip(),            
            'image_link' : image,          
            'auction_date' : auction_date,            
            'location' : location,           
            'product_name' : product_name,            
            'lot_id' : lot_number,          
            'auctioner' : auctioner,
            'website' : 'auctionresource',
            'description' : description             
        }