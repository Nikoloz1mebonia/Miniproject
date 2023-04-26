import requests
import datetime
import json
import sqlite3

api_key = "yXmbIthbp8bqjLGrT3EH39onLcDYFBFclP5nSFvR"
year = int(input("ფოტოსურათის გადაღების წელი: "))
month = int(input("სურათის გადაღების თვე: "))
day = int(input("სურათის გადაღების დღე: "))
date = datetime.date(year, month, day)
url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}"
# N1
r = requests.get(url)
print(r.status_code)
print(r.text)
print(r.headers)
# N2
r_loads = json.loads(r.text)
r_json = json.dumps(r_loads, indent=4)
f = open('json.file', 'w')
f.write(r_json)
f.close()
# N3
r_content = r.content
r_dict = json.loads(r_content)
print(f"სათაური: {r_dict['title']}; ფოტოს ლინკი: {r_dict['url']}, თარიღი: {date}")
# N4
# ამ კოდით იქმნება მონაცემთა ბაზა და ბაზაში არსებულ ცხრილში ემატება რამოდენიმე APOD
conn = sqlite3.connect("info_sqlite")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE information
(title  VARCHAR(100),
date  VARCHAR(10),
url_link VARCHAR(200)
);
""")
list1 = [
    ("Star Formation in the Tadpole Nebula", "2017-05-07",
     "https://apod.nasa.gov/apod/image/1705/ic410_WISEantonucci_960.jpg"),
    ("Earthset from Orion", "2022-11-23", "https://apod.nasa.gov/apod/image/2211/earthset-snap01.png"),
    ("Parker vs Perseid", "2018-08-16",
     "https://apod.nasa.gov/apod/image/1808/parkerlaunchperseids.apodDemeter1024.jpg")
]
cursor.executemany('INSERT INTO information(title, date, url_link) VALUES(?,?,?)', list1)
conn.commit()
conn.close()
