import os
import argparse
import csv
from requests import get
from bs4 import BeautifulSoup

zadana_url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
obsah = get(zadana_url)
rozdelene_html = BeautifulSoup(obsah.text, features="html.parser")
vsechna_td_cislo = rozdelene_html.find_all("td", {"class": "cislo"})
cisla_obci = [cislo.text for cislo in vsechna_td_cislo]

# def seznam_cisel_obci(zadana_url):
#     obsah = get(zadana_url)
#     rozdelene_html = BeautifulSoup(obsah.text, features="html.parser")
#     vsechna_td_cislo = rozdelene_html.find_all("td", {"class": "cislo"})
#     return [cislo.text for cislo in vsechna_td_cislo]

cislo_kraje = zadana_url.split("&")[-2].split("=")[-1]

# def cislo_kraje(zadana_url):
#     return zadana_url.split("&")[-2].split("=")[-1]

cislo_okresu= zadana_url.split("&")[-1].split("=")[-1]

# def cislo_okresu(zadana_url):
#     return zadana_url.split("&")[-1].split("=")[-1]


url_obci = [f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={cislo_kraje}&xobec={cislo_obce}&xvyber={cislo_okresu}" for cislo_obce in cisla_obci]

# def vsechna_url_k_vytěžení(cislo_kraje: str, cislo_okresu: str, cisla_obci: list):
#     return [f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={cislo_kraje}&xobec={cislo_obce}&xvyber={cislo_okresu}" for cislo_obce in cisla_obci]



obsah_obce = get(url_obci[0])
rozdelene_html_obce = BeautifulSoup(obsah_obce.text, features="html.parser")
obec = rozdelene_html_obce.select("h3")[2].get_text(strip=True).split(":")[1].strip()


hlavicka_1_cast = rozdelene_html_obce.find("table", {"id": "ps311_t1"}).find_all("tr")[0]
text_hlavicek = hlavicka_1_cast.get_text(separator=" ")
rozdel_a_panuj = text_hlavicek.split("\n")
seznam_hlav = [prvek.strip().lower() for prvek in rozdel_a_panuj if prvek]
# print(seznam_hlav)

hlavicka_2_cast_hodnoty = rozdelene_html_obce.find("table", {"id": "ps311_t1"}).find_all("tr")[2]
hodnoty_hlavicek = hlavicka_2_cast_hodnoty.get_text().strip()
rozdel_hodnoty_na_seznam = hodnoty_hlavicek.split("\n")
# print(rozdel_hodnoty_na_seznam)


tabulka = rozdelene_html_obce.find_all("table", {"class": "table"})
prvni_tabulka = tabulka[1]
vsechny_tr_tabulka1 = prvni_tabulka.find_all("tr")
# print(vsechny_tr_tabulka1)
vysledky_stran1 = {}
for tr in vsechny_tr_tabulka1[2:]:
    vsechna_td_v_jednotlivych_tr = tr.find_all("td")
    # print(vsechna_td_v_jednotlivych_tr)
    slovnik_stran1 = {vsechna_td_v_jednotlivych_tr[1].get_text(): vsechna_td_v_jednotlivych_tr[2].get_text()}
    vysledky_stran1.update(slovnik_stran1)
# print(vysledky_stran)


druha_tabulka = tabulka[2]
vsechny_tr_tabulka2 = druha_tabulka.find_all("tr")
vysledky_stran2 = {}
for tr in vsechny_tr_tabulka2[2:]:
    vsechna_td_v_jednotlivych_tr2 = tr.find_all("td")
    slovnik_stran2 = {vsechna_td_v_jednotlivych_tr2[1].get_text(): vsechna_td_v_jednotlivych_tr2[2].get_text()}
    vysledky_stran2.update(slovnik_stran2)
# print(vysledky_stran2)
# print(type(vysledky_stran2))


nadpisy_a_hodnoty = {"kód obce": cisla_obci[0], "název obce": obec, seznam_hlav[1]: rozdel_hodnoty_na_seznam[3], seznam_hlav[2]: rozdel_hodnoty_na_seznam[4], seznam_hlav[5]: rozdel_hodnoty_na_seznam[7]}
# print(nadpisy_a_hodnoty)

nadpisy_a_hodnoty.update(vysledky_stran1)
nadpisy_a_hodnoty.update(vysledky_stran2)
print(nadpisy_a_hodnoty)

