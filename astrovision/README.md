# 🔭 AstroVision – Katalog astronomických objektů

Ročníkový projekt – webová aplikace v Djangu pro správu a prohlížení katalogu astronomických objektů, pozorování a pozorovatelen.

## 📌 Téma

Aplikace slouží jako osobní astronomický katalog. Uživatel může procházet databázi deep-sky objektů (galaxie, mlhoviny, hvězdokupy), filtrovat je podle různých kritérií, zobrazit detailní informace a prohlédnout záznamy o minulých pozorováních.

## 🗄️ Datový model (5 propojených tříd)

| Model | Popis |
|-------|-------|
| `TypObjektu` | Kategorie objektu (galaxie, mlhovina, hvězdokupa…) |
| `Souhrezdí` | Souhvězdí, ve kterém se objekt nachází |
| `AstronomickyObjekt` | Hlavní objekt – FK na TypObjektu a Souhrezdí |
| `Pozorovatelna` | Lokalita / observatoř vhodná pro pozorování |
| `Pozorování` | Záznam pozorování – FK na AstronomickyObjekt a Pozorovatelna |

## 🖥️ Stránky aplikace

- `/` – Úvodní stránka se statistikami, doporučenými objekty a posledními pozorováními
- `/objekty/` – Výpis všech objektů s filtry (typ, souhvězdí, obtížnost, fulltextové hledání)
- `/objekty/<id>/` – Detail objektu s fyzikálními daty, pozorováními a příbuznými objekty
- `/pozorovateny/` – Výpis pozorovatelen seřazených dle světelného znečištění
- `/pozorovateny/<id>/` – Detail pozorovatelny s historií pozorování
- `/admin/` – Administrační rozhraní Django

## 🚀 Spuštění projektu

```bash
# 1. Klonování repozitáře
git clone https://github.com/<tvoje-uzivatelske-jmeno>/astrovision.git
cd astrovision

# 2. Vytvoření a aktivace virtuálního prostředí
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instalace závislostí
pip install -r requirements.txt

# 4. Migrace databáze
python manage.py migrate

# 5. Vytvoření superuživatele
python manage.py createsuperuser

# 6. (Volitelně) Načtení vzorových dat
python manage.py shell < load_sample_data.py

# 7. Spuštění vývojového serveru
python manage.py runserver
```

Aplikace poté běží na `http://127.0.0.1:8000/`
Administrace na `http://127.0.0.1:8000/admin/`

## 🛠️ Technologie

- **Python 3.12** + **Django 5.x**
- **SQLite3** (výchozí databáze)
- **Pillow** – práce s obrázky
- Čistý HTML/CSS frontend (žádný framework)

## 📁 Struktura projektu

```
astrovision/
├── astrovision/        # Nastavení projektu
│   ├── settings.py
│   └── urls.py
├── katalog/            # Hlavní aplikace
│   ├── models.py       # Datový model
│   ├── views.py        # Zobrazení (views)
│   ├── admin.py        # Administrace
│   ├── urls.py         # URL routing
│   ├── templates/      # HTML šablony
│   └── migrations/     # Databázové migrace
├── templates/          # Sdílená šablona base.html
├── static/             # Statické soubory
├── media/              # Nahrané obrázky
├── manage.py
├── requirements.txt
└── README.md
```

## 👤 Autor

Oliver Plaček – ročníkový projekt, 2025/2026
