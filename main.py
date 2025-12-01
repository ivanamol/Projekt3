import os
import argparse
import csv
from requests import get
from bs4 import BeautifulSoup

def zpracuj_odpoved_url(zadana_url: str) -> BeautifulSoup:
    obsah = get(zadana_url)
    return BeautifulSoup(obsah.text, features="html.parser")

def seznam_cisel_obci(soup):
    vsechna_td_cislo = soup.find_all("td", {"class": "cislo"})
    return [cislo.text for cislo in vsechna_td_cislo]

def cislo_kraje(zadana_url):
    return zadana_url.split("&")[-2].split("=")[-1]

def cislo_okresu(zadana_url):
    return zadana_url.split("&")[-1].split("=")[-1]

def url_tezba(zadana_url, soup_zadane_url):
    kraj = cislo_kraje(zadana_url)
    okres = cislo_okresu(zadana_url)
    seznam_obci = seznam_cisel_obci(soup_zadane_url)
    return [f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj}&xobec={obec}&xvyber={okres}" for obec in seznam_obci]

def ziskani_nazvu_obce(soap):
    return soap("h3")[2].get_text(strip=True).split(":")[1].strip()

def ziskani_dat_souhrn(soap):
    hlavicka = soap.find("table", {"id": "ps311_t1"}).find_all("tr")[2]
    hodnoty_hlavicek = hlavicka.get_text().strip()
    return hodnoty_hlavicek.split("\n")

def ziskani_dat_stran(soap):
    tabulka = soap.find_all("table", {"class": "table"})
    vysledky_stran2 = {}
    for index in range(1, 3):
        tabulka_cislo = tabulka[index]
        vsechny_tr_tabulka2 = tabulka_cislo.find_all("tr")
        for tr in vsechny_tr_tabulka2[2:]:
            vsechna_td_v_jednotlivych_tr2 = tr.find_all("td")
            vysledky_stran2[vsechna_td_v_jednotlivych_tr2[1].get_text()] = vsechna_td_v_jednotlivych_tr2[2].get_text()
    return vysledky_stran2

def uloz_do_csv(nazev_souboru, seznam_slovniku):
    with open(nazev_souboru, mode="w", newline="", encoding="UTF-8") as nove_csv:
        zahlavi = seznam_slovniku[0].keys()
        zapisovac = csv.DictWriter(nove_csv, fieldnames=zahlavi)
        zapisovac.writeheader()
        for slovnik in seznam_slovniku:
            zapisovac.writerow(slovnik)


zadana_url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101"

def main():
    odpoved_zadane_url = zpracuj_odpoved_url(zadana_url)
    cisla_obci = seznam_cisel_obci(odpoved_zadane_url)
    kompletni_slovnik = {}
    vysledek = []
    for jedna_samotinka_url in url_tezba(zadana_url, odpoved_zadane_url):
        odpoved_url_obce = zpracuj_odpoved_url(jedna_samotinka_url)
        nazev_obce = ziskani_nazvu_obce(odpoved_url_obce)
        ziskani_kodu_obce = jedna_samotinka_url.split("&")[-2].split("=")[-1]
        souhrn = ziskani_dat_souhrn(odpoved_url_obce)
        strany_slovnik = ziskani_dat_stran(odpoved_url_obce)
        uvodni_slovnik = {"kód obce": ziskani_kodu_obce, "název obce": nazev_obce, "voliči v seznamu": souhrn[3], "vydané obálky": souhrn[4], "platné hlasy": souhrn[7]}
        kompletni_slovnik = uvodni_slovnik | strany_slovnik
        vysledek.append(kompletni_slovnik)
    uloz_do_csv("volby.csv", vysledek)

if __name__ == "__main__":
    main()
