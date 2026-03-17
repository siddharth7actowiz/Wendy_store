from lxml import html 
from validation import Store
from pydantic import ValidationError
import re
from config import JSON_FILE_PATH
from utils import read_json
from pprint import pprint
import json
def parse_html(data):
    xpaths=read_json(JSON_FILE_PATH)
    parsed_data ={}
    tree = html.fromstring(data) 
    parsed_data["Name"]=tree.xpath(xpaths.get("Name_xapth")).strip()
    parsed_data["Map"]=tree.xpath(xpaths.get("Map_xapth")).strip()  
    parsed_data["StreetAddress"]=tree.xpath(xpaths.get("StreetAddress_xapth")).strip()  
    parsed_data["City"]=tree.xpath(xpaths.get("City_xapth")).strip()  
    parsed_data["State"]   = tree.xpath(xpaths.get("State_xapth")).strip()  
    parsed_data["Country"] = tree.xpath(xpaths.get("Country_xapth")).strip()  
    parsed_data["Pincode"]=tree.xpath(xpaths.get("Pincode_xapth")).strip()  
    Phone_num=tree.xpath(xpaths.get("Phone_Number_xapth")).strip()  
    phn_no = re.search(r'[\d\+\-\(\)\s]+', Phone_num)
    parsed_data["Phone_Number"] = phn_no.group().strip()
    #Restaurant Hours
    hours = {}
    rows = tree.xpath('.//tr[contains(@class,"c-location-hours-details-row")]')
    for row in rows:
        day= row.xpath('string(.//td[@class="c-location-hours-details-row-day"])').strip()
        open_t = re.sub(r'\s+', ' ', row.xpath('string(.//span[contains(@class,"instance-open")])').strip())
        close_t = re.sub(r'\s+', ' ', row.xpath('string(.//span[contains(@class,"instance-close")])').strip())
        hours[day] = f"{open_t} - {close_t}"

    parsed_data["Restaurant_Hours"] =  json.dumps(hours)
    
    #Drive Thru Hours
    dt_rows=tree.xpath('.//td[contains(@class,"c-location-hours-details-row js-day-of-week-row highlight-text highlight-background")]')
    dt_hours = {}
    dt_rows = tree.xpath('.//tr[contains(@class,"c-location-hours-details-row")]')
    for row in dt_rows:  # ← dt_rows not dt_hours
        day = row.xpath('string(.//td[contains(@class,"c-location-hours-details-row-day")])').strip()
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

       
    try:
        validated = Store(**parsed_data)   
        return validated.model_dump()      
    except ValidationError as e:
        print("Validation Error:", parse_html.__name__, e)
        return {} 

    

