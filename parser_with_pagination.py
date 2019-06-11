import requests
from bs4 import BeautifulSoup
import csv
import re


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text


def get_data(html):
    soup = BeautifulSoup(html,"lxml")
    lis = soup.find("ul", class_="clist").find_all("li")
    for li in lis:
        try:
            tds = li.find_all("td")
            name = tds[1].find("a").text
        except:
            name = ""
        try:
            city = tds[2].find_all("p")[-1].text
        except:
            city = ""
        try:
            phone = tds[2].find_all("p")[1].find_all("span", class_="contact-phone")[0].text.replace(" ","").\
                replace(",","").split()
        except:
            phone = ""

        data = {"city":city, "name":name, "phone":phone}

        write_csv(data)



def write_csv(data):
    with open("realtor_base.csv", "a") as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        writer.writerow([data["city"], data["name"], data["phone"]])


def main():
    url = "http://www.asnu.net/users/index/cat=1/asnu=1/"

    while True:
        get_data(get_html(url))

        soup = BeautifulSoup(get_html(url), "lxml")
        try:
            url = "http://www.asnu.net" + soup.find("ul", class_="menu-filter").\
                find("a", text=re.compile("следующая")).get("href")

        except:
            break


if __name__=="__main__":
    main()
