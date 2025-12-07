import argparse
import csv
from requests import get
from bs4 import BeautifulSoup
import sys

def getting_soup(url: str) -> BeautifulSoup:
    """
    It creates a BeautifulSoup object from the URL content.
    """
    contens = get(url)
    return BeautifulSoup(contens.text, features="html.parser")


def getting_municipalities_numbers(soup: BeautifulSoup) -> list:
    """
    It extracts all municipality numbers.
    """
    all_td_numbers = soup.find_all("td", {"class": "cislo"})
    return [number.text for number in all_td_numbers]


def getting_region_number(url: str) -> str:
    """
    It extracts the region number from the URL.
    """
    return url.split("&")[-2].split("=")[-1]


def getting_district_number(url: str) -> str:
    """
    It extracts the district number from the URL.
    """
    return url.split("&")[-1].split("=")[-1]


def url_mining(url: str, soup_url: BeautifulSoup) -> list:
    """
    It constructs the URL for each municipality and stores them in a list. It uses the URL and a list of municipality numbers.
    """
    region_number = getting_region_number(url)
    district_number = getting_district_number(url)
    list_of_municipalities = getting_municipalities_numbers(soup_url)
    return [f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={region_number}&xobec={municipality}&xvyber={district_number}" for municipality in list_of_municipalities]


def getting_name_of_municipality(soup: BeautifulSoup) -> str:
    """
    It gets the municipality names.
    """
    return soup("h3")[2].get_text(strip=True).split(":")[1].strip()


def getting_summary_data(soup: BeautifulSoup) -> list:
    """
    It extracts values from the summary election data in the municipality.
    """
    data_header = soup.find("table", {"id": "ps311_t1"}).find_all("tr")[2]
    values_in_data_header = data_header.get_text().strip()
    return values_in_data_header.split("\n")


def getting_political_parties_data(soup: BeautifulSoup) -> dict:
    """
    It gets the names and number of votes of individual political parties in the municipality.
    """
    table = soup.find_all("table", {"class": "table"})
    result_of_politicial_parties = {}
    for index in range(1, 3):
        for tr in table[index].find_all("tr")[2:]:
            result_of_politicial_parties[tr.find_all("td")[1].get_text()] = tr.find_all("td")[2].get_text()
    return result_of_politicial_parties


def save_to_csv(file_name: str, list_of_dictionaries: list) -> None:
    """
    It iteratively saves each dictionary from the list of dictionaries to a csv file.
    """
    print(f"UKLÁDÁM DO SOUBORU: {file_name}")
    with open(file_name, mode="w", newline="", encoding="UTF-8") as new_csv:
        table_header = list_of_dictionaries[0].keys()
        writer_csv = csv.DictWriter(new_csv, fieldnames=table_header)
        writer_csv.writeheader()
        for dictionary in list_of_dictionaries:
            writer_csv.writerow(dictionary)


def chceck_input_arguments(url: str, file_name:str) -> None:
    """
    It checks whether the url is specified in the correct argument and whether it starts with the correct format. In case of an incorrect entry, the program terminates.
    """
    if file_name.startswith("https://"):
        print("The value provided for --file_name appears to be a URL, not a file name.")
        return sys.exit()
    elif not url.startswith("https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj="):
        print("Invalid URL provided for --url argument. Correct format example: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103")
        return sys.exit()
    else:
        None


def check_error_url(url):
    """
    "It checks whether an error code is returned or error message is returned with code 200. In case of an error code or message, the program terminates."
    """
    contens = get(url)
    status_response = contens.status_code
    if status_response == 200:
        soup = BeautifulSoup(contens.text, features="html.parser")
        html_h3 = soup.find("h3")
        text_h3 = html_h3.get_text()
        if "Page not found!" not in text_h3:
            return print(f"STAHUJI DATA Z VYBRANEHO URL: {url}")
        else:
            print("The server returned code 200 for the specified URL, but the page contains the error message 'Page not found!'.\nTerminating the program.")
            sys.exit()
    else:
        print(f"The server returned code {status_response} for the specified URL.\nTerminating the program.")
        sys.exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    parser.add_argument("--file_name", type=str, required=True)
    args = parser.parse_args()
    chceck_input_arguments(args.url, args.file_name)
    check_error_url(args.url)
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
    print(f"UKONČUJI {sys.argv[0].split(".")[0]}")
    sys.exit()


if __name__ == "__main__":
    main()

