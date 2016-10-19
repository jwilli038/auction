# Okaloosa County Auctions
# import modules
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import quandl
import numpy as np
import matplotlib.pyplot as plt

# initialize
url = 'https://auction.com/residential/fl/okaloosa-county'

#open and read
openedUrl = urlopen(url)
soup = BeautifulSoup(openedUrl, 'html.parser')
branchUrls = re.findall('https://www.auction.com/details/(.*?)"',str(soup))
threeBedroomData = quandl.get("ZILL/CO03168_3B")
tbD = plt.plot(threeBedroomData)
        
#open each listing and scrape data
for link in branchUrls:
    url = 'https://www.auction.com/details/' + link
    openedUrl = urlopen(url)
    soup = BeautifulSoup(openedUrl, 'html.parser')
    details = soup.findAll("div", attrs={"class":"propertyDetailTable propDetailsLeft"})
    street = str(soup.find('span', attrs={'class':'address-header1'})).split('>')[1].split('<')[0]
    location = str(soup.find('span', attrs={'class':'address-header2'})).split('>')[1].split('<')[0]
    propertyType = re.findall('data-elm-id="property_type">(.*?)<',str(details))
    beds = re.findall('data-elm-id="bedrooms">(.*?)<',str(details))
    baths = re.findall('data-elm-id="baths">(.*?)<',str(details))
    year = re.findall('data-elm-id="year_built">(.*?)<',str(details))
    sqFeet = re.findall('data-elm-id="home_square_footage">(.*?)<',str(details))
    lotSize =  re.findall('data-elm-id="lot_size">(.*?)<',str(details))
    #auctionData = re.findall('data-elm-id="auction_start_date">(.*?)<',openedUrl)
    try:
        cost = str(soup.findAll(text = "Final Judgment Amount")[0].parent.parent).split('$')[1].split('<')[0]
    except:
        cost = 'not listed'
    print(street, location, propertyType, beds, baths, year, sqFeet, lotSize, cost)
    if beds == [' 3']:
        try:
            price = np.vstack((price,float(cost.replace(',',''))))
        except:
            try:
                price = float(cost.replace(',',''))
            except:
                print('not listed')
        
