import scrapy
from scrapy_selenium import SeleniumRequest
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from scrapy.shell import inspect_response
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ExhibitorSpider(scrapy.Spider):
    name = 'exhibitor'
    x = 1
    unscraped_links = [] # ones who don't have website...


    def start_requests(self):
        yield SeleniumRequest(
        url='http://www.ifema.es/en/fitur/exhibitors-catalogue/',
        wait_time=3,
        screenshot=False,
        callback=self.parse)

    def parse(self, response):
        self.driver =response.meta['driver']
        
        try:
            self.driver.find_element_by_id('onetrust-accept').click()
        except:
            pass
        time.sleep(3)
        try:
            self.driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/div/div[2]/a').click()
        except:
            pass
        time.sleep(3)
        # inspect_response(response, self)
        self.driver.set_window_size(1920, 1080)
        iframe = self.driver.find_element_by_css_selector('div.iframe-container > iframe')
        self.driver.switch_to.frame(iframe)
        static_first_part = self.driver.find_elements_by_css_selector('div#__next > div > div:nth-of-type(2) > div > div > div > div:nth-of-type(1) > a')
        dynamic_second_part = self.driver.find_element_by_css_selector('div#__next > div > div:nth-of-type(2) > div > div > div > div:nth-of-type(2)')
        a = dynamic_second_part.find_element_by_css_selector('a')

        for url in self.unscraped_links:
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div/div[text()="Activity sector"]/following-sibling::div/div/div/span')))
                yield self.exhibitor(Selector(text=self.driver.page_source)) 
            except:
                print(f'\n\n\n error start ({url})\n')
                traceback.print_exc()
                self.unscraped_links.append(url)
                print('\nerror finish\n\n\n')
        
        print(self.unscraped_links)
            
    def exhibitor(self, response):
        print('reached here \n')
        print(f'{self.x}th')
        self.x += 1
        name = response.xpath('//h1/text()').get()
        activity_sectors = response.xpath('//div/div[text()="Activity sector"]/following-sibling::div/div/div/span/text()').get()

        print('\n')
        print({
            'Company Name': name,
            # 'Website': website,
            'Activity Sectors': activity_sectors
        })
        print('\n')
        return {
            'Company Name': name,
            # 'Website': website,
            'Activity Sectors': activity_sectors
        }
