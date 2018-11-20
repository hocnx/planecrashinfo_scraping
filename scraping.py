
import requests
from bs4 import BeautifulSoup
import datetime
import csv
import progressbar
from time import sleep


def request_to_server(url):
    response = None
    try:
        response = requests.get(url, timeout=10)
        return response
    except :
        print("sleep for 10 seconds")
        sleep(10)
        response = request_to_server(url)
        return response

base_uri = "http://www.planecrashinfo.com"
year_data = {}
csv_writer = csv.writer(open("planecrashinfo_"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".csv", 'w'))

# write data header to csv file
csv_writer.writerow(["date","time","location","operator","flight_no","route","ac_type","registration","cn_ln","aboard","fatalities","ground","summary"])

# request to list of years
response = request_to_server("http://www.planecrashinfo.com/database.htm")


if(response.status_code == 200):
    parser = BeautifulSoup(response.content, 'html.parser')
    a_tags = parser.find_all("a")
    # build a dict contain the year as key and page url as value
    year_data = {a.text.strip():{"url":base_uri + a["href"] if a["href"][0]=="/" else base_uri + "/" +a["href"] } for a in a_tags if a.text.strip().isdigit()}

    # loop for each year
    for year, data in year_data.items():

        # request to list of year's crashes
        response_year = request_to_server(data["url"])
        parser_year = BeautifulSoup(response_year.content, 'html.parser')

        # get all <a> tag except  "Return to Home" link
        a_tags = parser_year.find_all("a")
        a_tags = [a for a in a_tags if "Return to Home" not in a.text]

        # progress bar initial
        i = 0
        bar = progressbar.ProgressBar(maxval=len(a_tags), \
            widgets=[year +": ",progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        for a in a_tags:
            #print("-", sep=' ', end='', flush=True)


            # request to crash detail page
            response_crash = request_to_server(base_uri + "/" + year  + a["href"] if a["href"][0] == "/" else base_uri + "/" + year + "/" + a["href"])
            parser_crash = BeautifulSoup(response_crash.content, 'html.parser')

            # get all table content except the first row(table title)
            tr_tags = parser_crash.find_all("tr")
            tr_tags = tr_tags[1:]

            # write data to csv file
            data = [tr.find_all("td")[1].text.strip() for tr in  tr_tags]
            csv_writer.writerow(data)

            # update the bar
            bar.update(i+1)
            i = i+1

            # sleep to overcome Server connection refused error
            sleep(0.1)

        bar.finish()
else:
    print("Cannot fetch data")
