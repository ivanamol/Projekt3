# Projekt3
Třetí projekt online kurzu Tester s Pythonem od Engeta.
## Popis projektu
Cílem je vytvořit scraper výsledků voleb z roku 2017, který data vytáhne přímo z webu. Odkaz k prohlédnutí najdete [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).
Skript umí vybrat jakýkoliv územní celek z hlavní tabulky a následně vyscrapuje výsledky hlasování pro všechny obce daného celku.
## Instalace knihoven
V kódu použité knihovny jsou uloženy v souboru [requirements.txt](requirements.txt). Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
```
$ pip --version                    # overim verzi manazeru
$ pip install -r requirements.txt  # nainstalujeme knihovny
```
## Spuštění projektu
Spuštění souboru `main.py` v rámci příkazové řádky požaduje dva povinné argumenty. Využívá se knihovny argparse. Jméno souboru se zadává s příponou .csv
```
python main.py --url <odkaz-uzemniho-celku> --file_name <vysledny-soubor>
```

Následně se výsledky stáhnou jakou soubor s příponou `.csv`.
## Ukázka projektu
Výsledky hlasování pro okres Prostějov:
1. argument `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103`
2. argument `vysledky_prostejov.csv`
   
Spuštění programu:
```
python main.py --url "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" --file_name "vysledky_prostejov.csv"
```
Průběh stahování:
```
STAHUJI DATA Z VYBRANEHO URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
UKLADAM DO SOUBORU: vysledky_prostejov.csv
UKONCUJI main
```
Částečný výstup:
```
code,location,registered,envelopes,valid,...
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
...
```


