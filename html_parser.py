from lxml import html 
from validation import Store
from pydantic import ValidationError
import re
from pprint import pprint
import json
def parse_html(data):
    parsed_data ={}
    tree = html.fromstring(data) 
    parsed_data["Name"]=tree.xpath('string(.//h1[@class="HeroBanner-title Heading--lead"])').strip()
    parsed_data["Map"]=tree.xpath('string(.//div[@class="c-get-directions-button-wrapper"]/a[@class="c-get-directions-button"]/@href)').strip()  
    parsed_data["StreetAddress"]=tree.xpath('string(.//span[@class="c-address-street-1"])').strip()
    parsed_data["City"]=tree.xpath('string(.//span[@class="c-address-city"])').strip()
    parsed_data["State"]   = tree.xpath('string(.//abbr[contains(@class,"c-address-state")])').strip()
    parsed_data["Country"] = tree.xpath('string(.//abbr[contains(@class,"c-address-country-name")])').strip()
    parsed_data["Pincode"]=tree.xpath('string(.//span[@class="c-address-postal-code"])')
    Phone_num=tree.xpath('string(.//a[@class="c-phone-number-link c-phone-main-number-link"]/@href)')
    phn_no = re.search(r'[\d\+\-\(\)\s]+', Phone_num)
    parsed_data["Phone_Number"] = phn_no.group().strip()
    #Restaurant Hours
    hours = {}
    rows = tree.xpath('.//tr[contains(@class,"c-location-hours-details-row")]')
    for row in rows:
        day     = row.xpath('string(.//td[@class="c-location-hours-details-row-day"])').strip()
        open_t  = re.sub(r'\s+', ' ', row.xpath('string(.//span[contains(@class,"instance-open")])').strip())
        close_t = re.sub(r'\s+', ' ', row.xpath('string(.//span[contains(@class,"instance-close")])').strip())
        hours[day] = f"{open_t} - {close_t}"

    parsed_data["Restaurant_Hours"] =  json.dumps(hours)
    
    #Drive Thru Hours
    dt_rows=tree.xpath('.//td[contains(@class,"c-location-hours-details-row js-day-of-week-row highlight-text highlight-background")]')
    dt_hours = {}
    dt_rows = tree.xpath('.//tr[contains(@class,"c-location-hours-details-row")]')
    for row in dt_rows:  # ← dt_rows not dt_hours
        day     = row.xpath('string(.//td[contains(@class,"c-location-hours-details-row-day")])').strip()
        open_t  = re.sub(r'\s+', ' ', row.xpath('string(.//span[contains(@class,"instance-open")])').strip())
        close_t = re.sub(r'\s+', ' ', row.xpath('string(.//span[contains(@class,"instance-close")])').strip())
        dt_hours[day] = f"{open_t} - {close_t}"

    parsed_data["DriveThru_Hours"] =  json.dumps(dt_hours)

    
     # Delivery Options
    delivery_list = []
    for delivery in tree.xpath('//a[contains(@class,"delivery")]'):
        delivery_list.append(delivery.xpath('string(./@href)').strip())
    parsed_data["DeliveryOption"] =  json.dumps(delivery_list)  # ← serialized

    # Currently Operating
    operating_list = []
    for operating in tree.xpath('//li[@class="LocationInfo-service"]'):
        operating_list.append(
            operating.xpath('string(.//span[contains(@itemprop,"amenityFeature")])').strip()
        )
    parsed_data["CurrentlyOperating"] = json.dumps(operating_list)  # ← serialized

    #Menu Data

    menu_data = []
    for item in tree.xpath('.//li[contains(@class,"ProductList-listItem")]'):
        menu_item = {}
        menu_item["Name"]        = item.xpath('string(.//span[contains(@class,"Product-titleText")])').strip()
        menu_item["Description"] =  re.sub(r'\s+', ' ', item.xpath('string(.//div[contains(@class,"Product-text")])')).strip()
        menu_item["URL"]         = item.xpath('string(.//a[contains(@class,"Product-link")]/@href)').strip()
        menu_item["Image"]       = item.xpath('string(.//img[contains(@class,"Product-img")]/@src)').strip()
        menu_data.append(menu_item)
    parsed_data["Menu_Items"]= json.dumps(menu_data)    
    

    
    try:
        validated = Store(**parsed_data)   # ← ** unpacks dict as kwargs
        return validated.model_dump()      # ← return outside try, after validation
    except ValidationError as e:
        print("Validation Error:", parse_html.__name__, e)
        return {} 

    

