
import requests
from bs4 import BeautifulSoup
import datetime

response = requests.get("http://www.planecrashinfo.com/database.htm")
base_uri = "http://www.planecrashinfo.com"
year_data = {}

f = open("planecrashinfo_"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".csv", "w")
f.write("date,time,location,operator,flight_no,route,ac_type,registration,cn_ln,aboard,fatalities,ground,summary\n")


if(response.status_code == 200):
    parser = BeautifulSoup(response.content, 'html.parser')
    a_tags = parser.find_all("a")
    year_data = {a.text.strip():{"url":base_uri + a["href"] if a["href"][0]=="/" else base_uri + "/" +a["href"] } for a in a_tags if a.text.strip().isdigit()}

    for year, data in year_data.items():
        print(year, data["url"])
        #td_tags = parser.find_all("tr")
        response_year = requests.get(data["url"])
        parser_year = BeautifulSoup(response_year.content, 'html.parser')

        a_tags = parser_year.find_all("a")
        a_tags = [a for a in a_tags if "Return to Home" not in a.text]
        for a in a_tags:
            response_crash = requests.get(base_uri + "/" + year  + a["href"] if a["href"][0] == "/" else base_uri + "/" + year + "/" + a["href"])
            parser_crash = BeautifulSoup(response_crash.content, 'html.parser')
            tr_tags = parser_crash.find_all("tr")
            tr_tags = tr_tags[1:]
            last_item = len(tr_tags)
            for i in range(0,last_item):
                f.write('"'+tr_tags[i].find_all("td")[1].text.strip()+'"')
                if i == last_item-1 :
                    f.write("\n")
                else:
                    f.write(",")

else:
    print("Cannot fetch data")
