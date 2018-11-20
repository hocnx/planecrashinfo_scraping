# planecrashinfo_scraping
http://www.planecrashinfo.com/database.htm

There are some big plane crashes recently.
I want to know more about the crashes.
For very first step, I need to collect data from somewhere, then I found planecrashinfo.com.
In this project, I will use Python, BeautifulSoup to collect data from  planecrashinfo.com
Data format
```
Format
date:	 Date of accident,  in the format - January 01, 2001
time:	 Local time, in 24 hr. format unless otherwise specified
location: location information
Airline/Op:	 Airline or operator of the aircraft
flight_no:	 Flight number assigned by the aircraft operator
route:	 Complete or partial route flown prior to the accident
ac_type:	 Aircraft type
registration:	 ICAO registration of the aircraft
cn_ln:	 Construction or serial number / Line or fuselage number
aboard:	 Total aboard (passengers / crew)
fatalities:	 Total fatalities aboard (passengers / crew)
ground:	 Total killed on the ground
summary:	 Brief description of the accident and cause if known
```

f.write("date,time,location,operator,flight_no,route,ac_type,registration,cn_ln,aboard,fatalities,ground,summary\n")

## Prerequisites
```
python 3
```
## Installing
```
virtualenv -p python3 .myenv

source .myenv/bin/activate

pip install -r requirements.txt
```
## Running
```
python scraping.py
```
