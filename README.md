<!-- omit in toc -->
# ⚽ Football Analysis Project

Analýza futbalovej štatistiky - TOP tímy a hráči z ceľého sveta podľa pozícií.

**Technológie:** Python, Pandas, Matplotlib

---

## 📋 Obsah

- [Čo to je?](#čo-to-je)
- [Ako nainštalovať?](#ako-nainštalovať)
- [Ako spustiť?](#ako-spustiť)
- [Čo analýza robí?](#čo-analýza-robí)
- [Výstupy](#výstupy)
- [Súbory projektu](#súbory-projektu)
- [Budúce vylepšenia](#budúce-vylepšenia)

---

## Čo to je?

Projekt analyzuje dáta o futbalových útočníkoch (pozícia **FW - Forward**) zo svetového pohľadu. Zisťuje:

✅ Ktoré tímy majú najviac gólov?  
✅ Aká je priemerná výška útočníkov?  
✅ Či majú skúsenejší hráči viac gólov?  
✅ Kto sú TOP 10 najlepší skóreri?

---

## Ako nainštalovať?

### 1️⃣ Klonuj projekt

```bash
git clone https://github.com/denishorsky98-cmd/football-analysis.git
cd football-analysis
```

### 2️⃣ Vytvor Python virtual environment

```bash
python -m venv venv
```

### 3️⃣ Aktivuj virtual environment

**Na Windows:**
```bash
venv\Scripts\activate
```

**Na macOS/Linux:**
```bash
source venv/bin/activate
```

### 4️⃣ Nainštaluj dependencies

```bash
pip install -r requirements.txt
```

---

## Ako spustiť?

```bash
python analysis.py
```

**Výstup:**
- 📊 Detailné štatistiky v konzole
- 📈 4 grafy uložené ako `football_analysis.png`

---

## Čo analýza robí?

### 📊 Graf 1: TOP 10 Tímov podľa Gólov
Zobrazuje ktoré tímy majú najviac gólov medzi útočníkmi (FW).

### 📏 Graf 2: Distribúcia Výšky Útočníkov
Histogram s distribúciou výšky a zvýrazneným priemerom.

### ⚽ Graf 3: Góly vs. Skúsenosť (Caps)
Scatter plot - väzbosť medzi počtom zápasov (Caps) a počtom gólov.

### 🏆 Graf 4: TOP 10 Hráčov podľa Gólov
Horizontálny bar chart s najlepšími 10 hráčmi.

---

## Výstupy

```
📊 Celkový počet útočníkov: XXX
📏 Priemerná výška: XXX.X cm
⚽ Priemer gólov na hráča: XX.X
🎮 Priemer Caps na hráča: XX.X

TOP 10 TÍMOV PODĽA GÓLOV:
[Tabuľka s tímami a počtom gólov]

TOP 10 HRÁČOV PODĽA GÓLOV:
[Tabuľka s hráčmi a počtom gólov]

✅ Všetky grafy uložené ako 'football_analysis.png'
```

---

## Súbory projektu

```
football-analysis/
├── analysis.py                 # Hlavný skript s analýzou
├── SquadLists.csv             # Dataset s dátami hráčov
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore súbory
├── README.md                   # Táto dokumentácia
├── football_analysis.png       # Vygenerované grafy (output)
├── goals_by_team.png           # Dodatočný graf (output)
└── Readme.dm                   # (starý format)
```

### 📄 Popis súborov

| Súbor | Popis |
|-------|-------|
| `analysis.py` | Hlavný Python skript s analýzou dát a vytváraním grafov |
| `SquadLists.csv` | Dataset obsahujúci dáta o hráčoch (meno, tím, pozícia, výška, góly, caps) |
| `requirements.txt` | Zoznam Python balíčkov potrebných na spustenie |
| `.gitignore` | Súbory, ktoré Git ignoruje (obrázky, cache, venv) |
| `README.md` | Dokumentácia projektu (táto súbor) |

---

## Štruktúra CSV

Súbor `SquadLists.csv` obsahuje nasledujúce stĺpce:

```
Player Name | Team | Position | Height (cm) | Goals | Caps | ...
```

**Pozície:**
- `FW` - Forward (Útočník) ⚽
- `MF` - Midfielder (Stredopoliar)
- `DF` - Defender (Obranca)
- `GK` - Goalkeeper (Brankár)

---

## Budúce vylepšenia

- [ ] Analýza iných pozícií (MF, DF, GK)
- [ ] Porovnanie podľa krajín
- [ ] Korelačná analýza (výška vs. góly)
- [ ] Interaktívne grafy (Plotly)
- [ ] Web dashboard (Flask/Streamlit)
- [ ] Automatické testy (pytest)
- [ ] GitHub Actions CI/CD

---

## 🔧 Troubleshooting

**Chyba: `ModuleNotFoundError: No module named 'pandas'`**
```bash
pip install -r requirements.txt
```

**Chyba: `FileNotFoundError: SquadLists.csv`**
Skontroluj že `SquadLists.csv` je v rovnakom priečinku ako `analysis.py`.

**Grafy sa neukazujú**
Skontroluj či máš nainštalovaný matplotlib:
```bash
pip install matplotlib
```

---

## 📧 Kontakt

Autor: **denishorsky98-cmd**  
GitHub: https://github.com/denishorsky98-cmd

---

## 📝 Licencia

Tento projekt je voľne dostupný.

---

**Posledná aktualizácia:** September 2026
