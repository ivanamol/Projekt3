# Projekt3
Třetí projekt online kurzu Tester s Pythonem od Engeta.
## Popis projektu
Cílem je vytvořit scraper výsledků voleb z roku 2017, který data vytáhne přímo z webu.
Skript umí vybrat jakýkoliv územní celek z hlavní tabulky a následně vyscrapuje výsledky hlasování pro všechny obce daného celku.
## Instalace knihoven
V kódu použité knihovny jsou uloženy v souboru requirements.txt. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
```
$ pip --version                      # overim verzi manazeru
$ pip install -r requirements.txt    # nainstalujeme knihovny
```
# Spuštění projektu
Spuštění souboru main.py v rámci příkazové řádky požaduje dva povinné argumenty. Využívá se knihovny argparse.
python main.py --url <odkaz-uzemniho-celku> --file_name <vysledny-soubor>
Následně se výsledky stáhnou jakou soubor s příponou.csv.
