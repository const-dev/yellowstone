from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import itertools


def check_hotel(hotel, date, month='August', year='2013', adults=4):
    driver = webdriver.Firefox()
    #driver = webdriver.PhantomJS('phantomjs')

    driver.get('http://www.yellowstonenationalparklodges.com')

    driver.find_element_by_xpath(
            '//select[@id="pDestId_h"]/option[text()="%s"]' % 
            hotel).click()

    driver.find_element_by_xpath(
            '//select[@id="ArvMonth"]/option[text()="%s - %s"]' %
            (year, month)).click()

    driver.find_element_by_xpath(
            '//select[@id="ArvDate"]/option[text()="%d"]' % 
            date).click()

    driver.find_element_by_xpath(
            '//select[@id="number_adults"]/option[text()="%s"]' % 
            adults).click()

    driver.find_element_by_id('x_Check_Availability').submit()

    try:
        WebDriverWait(driver, 180).until(
                EC.presence_of_element_located((By.ID, 'roomlist')))

        # Make sure the alert pops up if it is going to.
        time.sleep(1)

        try:
            alert = driver.switch_to_alert()
            #print alert.text
            alert.accept()
        #except NoAlertPresentException:
        #    # Guess if there is no alert, there might be a room available.
        #    print 'no alert: %s' % hotel
        except Exception:
            # Message: u'a is null'. What the heck is this?
            pass

        reserve_xpath = '//input[@value="RESERVE NOW"]'

        reserve_buttons = driver.find_elements_by_xpath(reserve_xpath)


        if len(reserve_buttons) > 0:
            print time.strftime('[%Y-%m-%d %H:%M:%S]'),
            print '%s %02d %s: %d' % (month, date, hotel, 
                                      len(reserve_buttons))

            prefix = reserve_xpath + '/parent::*' * 8

            hotel_types = [
                    hotel_type.text 
                    for hotel_type in driver.find_elements_by_xpath(
                        prefix + '//tr[@class="bgwhite"]' + 
                        '//span[@class="normal11 bold"]')]

            prizes = [
                    prize.text 
                    for prize in driver.find_elements_by_xpath(
                        prefix + '//tr[@class="bglight"]' +
                        '//td[1]/span[@class="normal10 bold"]')]

            for hotel_type, prize in zip(hotel_types, prizes):
                print '%s: %s' % (hotel_type, prize)

    except Exception as e:
        # Just in case..
        #print e
        pass

    finally:
        driver.quit()


def main():

    ## Test case #1:
    #hotels = ['Grant Village',
    #          'Old Faithful Snow Lodge',
    #         ]
    #dates = [25]
    #month = 'September'

    ## Test case #2:
    #hotels = ['Old Faithful Snow Lodge']
    #dates = [19]
    #month = 'December'

    hotels = ['Canyon Lodge',
              'Grant Village',
              'Lake Hotel and Cabins',
              'Lake Lodge',
              'Mammoth Hotel and Cabins',
              'Old Faithful Inn',
              'Old Faithful Lodge',
              'Old Faithful Snow Lodge',
              'Roosevelt Lodge',
             ]

    dates = [9, 10, 11, 12, 13]
    month = 'August'

    for i in xrange(10):
        for date, hotel in itertools.product(dates, hotels):
            check_hotel(hotel, date=date, month=month)
            time.sleep(2)
        time.sleep(60 * 20)


if __name__ == '__main__':
    main()
