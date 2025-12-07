import argparse
import csv
from requests import get
from bs4 import BeautifulSoup

def getting_soup(url: str) -> BeautifulSoup:
    contens = get(url)
    return BeautifulSoup(contens.text, features="html.parser")

def getting_municipalities_numbers(soup):
    all_td_numbers = soup.find_all("td", {"class": "cislo"})
    return [number.text for number in all_td_numbers]

def getting_region_number(url):
    return url.split("&")[-2].split("=")[-1]

def getting_district_number(url):
    return url.split("&")[-1].split("=")[-1]

def url_mining(url, soup_url):
    region_number = getting_region_number(url)
    district_number = getting_district_number(url)
    list_of_municipalities = getting_municipalities_numbers(soup_url)
    return [f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={region_number}&xobec={municipality}&xvyber={district_number}" for municipality in list_of_municipalities]

def getting_name_of_municipality(soup):
    return soup("h3")[2].get_text(strip=True).split(":")[1].strip()

def getting_summary_data(soup):
    data_header = soup.find("table", {"id": "ps311_t1"}).find_all("tr")[2]
    values_in_data_header = data_header.get_text().strip()
    return values_in_data_header.split("\n")


def getting_political_parties_data(soup):
    table = soup.find_all("table", {"class": "table"})
    result_of_politicial_parties = {}
    for index in range(1, 3):
        for tr in table[index].find_all("tr")[2:]:
            result_of_politicial_parties[tr.find_all("td")[1].get_text()] = tr.find_all("td")[2].get_text()
    return result_of_politicial_parties

def save_to_csv(file_name, list_of_dictionaries):
    with open(file_name, mode="w", newline="", encoding="UTF-8") as new_csv:
        table_header = list_of_dictionaries[0].keys()
        writer_csv = csv.DictWriter(new_csv, fieldnames=table_header)
        writer_csv.writeheader()
        for dictionary in list_of_dictionaries:
            writer_csv.writerow(dictionary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str)
    parser.add_argument("--file_name", type=str)
    args = parser.parse_args()
    soup_specified_url = getting_soup(args.url)
    complete_dictionary = {}
    result = []
    for single_url in url_mining(args.url, soup_specified_url):
        soup_municipality = getting_soup(single_url)
        election_summary = getting_summary_data(soup_municipality)
        political_parties_dictionary = getting_political_parties_data(soup_municipality)
        election_summary_dictionary = {"code": single_url.split("&")[-2].split("=")[-1], "location": getting_name_of_municipality(soup_municipality), "registered": election_summary[3], "envelopes": election_summary[4], "valid": election_summary[7]}
        complete_dictionary = election_summary_dictionary | political_parties_dictionary
        result.append(complete_dictionary)
    save_to_csv(args.file_name, result)


if __name__ == "__main__":
    main()

