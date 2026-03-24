
# Vežbe 02 – NumPy, Pandas i Matplotlib

Ove tri biblioteke smatraju se osnovom analize podataka u programskom jeziku Python:

* `NumPy` se koristi za efikasan rad  sa numeričkim podacima (vektori, matrice, linearna algebra)
* `Pandas` se koristi za rad sa tabelarnim podacima (CSV/Excel, filtriranje, grupisanje)
* `Matplotlib` se koristi za vizuelizaciju podataka (grafici, histogrami, scatter)

---

## 1. NumPy: kako se koristi i čemu je namenjen

Tip podataka `ndarray` (N-dimensional array) uvodi se u `NumPy`, pri čemu je definisan kao:

* homogen (svi elementi se održavaju u istom tipu)
* kompaktno smešten u memoriji
* veoma brz za numeričke operacije

### Kako funkcioniše

Za razliku od Python listi, podaci se u `ndarray` strukturi čuvaju u kontinualnom bloku memorije, a operacije se izvršavaju pomoću optimizovanih funkcija napisanih u C-u.
Time se omogućava da budu:

* brže operacije nad velikim nizovima
* vektorizacija operacije (`a + b`, `a * b`, `np.sqrt(a)`) bez eksplicitnih `for` petlji
* automatsko usklađivanje dimenzija tokom operacija

### Glavne namene

* vektori i matrice predstavljaju se `ndarray` strukturom
* operacije linearne algebre (`dot`, inverzija, rešavanje sistema) izvršavaju se efikasno
* numerička priprema podataka za mašinsko učenje
* osnova brojnih biblioteka (`pandas`, `scikit-learn`, `tensorflow`) 

### Ključni pojmovi

* `shape`: dimenzije niza
* `dtype`: tip elemenata
* `slicing`: podnizovi
* `axis`: smer primene operacija (`sum`, `mean`, …)

---

## 2. Pandas: kako se koristi i čemu je namenjen

`Pandas` je osmišljen za rad sa tabelarnim podacima.
Dve osnovne strukture podatakau biblioteci:

* `Series`: jedna kolona (1D)
* `DataFrame`: tabela sa vrstama i kolonama (2D)

### Kako funkcioniše

Podaci se u biblioteci `Pandas` čuvaju korišćenjem `NumPy` struktura, dok se dodatno omogućava:

* korišćenje označenih kolona i indeksa
* učitavanje podataka pomoću funkcija (`read_csv`, `read_excel`, …)
* primena API-ja za filtriranje, sortiranje, grupisanje i transformacije

### Glavne namene

* skupovi podataka učitavaju se i pregledaju kroz `DataFrame`
* čišćenje podataka (nedostajuće vrednosti, promene tipova, mapiranja)
* izdvajanje atributa (`X`) i ciljne promenljive (`y`)
* agregacije i grupisanje preko `groupby`
* priprema podataka za modele mašinskog učenja

### Ključni pojmovi

* `iloc`: indeksiranje po poziciji
* `loc`: indeksiranje po oznakama (nazivima kolona)
* `Series` vs `DataFrame`: jedna kolona naspram kompletne tabele

---

## 3. Matplotlib: kako se koristi i čemu je namenjen

`Matplotlib` predstavlja osnovnu biblioteku za crtanje grafikona u Python-u.

### Kako funkcioniše

Najčešće se koristi modul `matplotlib.pyplot`, kojim se omogućava interfejs sličan MATLAB-u:

* kreira se figura
* dodaju se podaci za iscrtavanje (`plot`, `scatter`, `hist`, …)
* dodaju se oznake (`title`, `xlabel`, `ylabel`, `legend`)
* grafikon se prikazuje pomoću `show`

Podržan je i objektno-orijentisani API (`fig`, `ax`), koji se koristi za složenije prikaze i više podgrafika (`subplots`).

### Glavne namene

* vizuelna analiza podataka
* funkcije i modeli porede se vizuelnim prikazima
* obrasci, odstupanja i greške lakše se otkrivaju na grafikonima
* grafikoni za izveštaje i prezentacije izrađuju se standardizovano

### Najčešći tipovi grafika

* linijski grafik (`plot`) 
* tačkasti grafik (`scatter`) 
* histogram (`hist`)
* stubičasti grafik (`bar`)

---

## Kako ove biblioteke funkcionišu zajedno

Tipičan tok rada na kursu zasniva se na sledećem:

1. podaci se učitavaju i pripremaju u `Pandas` (`DataFrame`)
2. numeričke transformacije nad kolonama i nizovima izvršavaju se u `NumPy`
3. rezultati i obrasci vizuelno se prikazuju putem `Matplotlib`

Praktično, `Pandas` i `Matplotlib` funkcionišu oslanjajući se na `NumPy`, pa se ove biblioteke prirodno uklapaju u jedinstven ekosistem.

---

## Instalacija i pokretanje

Rad u virtuelnom okruženju preporučuje se:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install numpy pandas matplotlib jupyterlab
```

Pokretanje okruženja:

```bash
jupyter lab
```

## Materijali

* `01_numpy.ipynb` – uvod u `NumPy`
* `02_matplotlib.ipynb` – uvod u `Matplotlib`
* `03_pandas.ipynb` – uvod u `Pandas` i rad sa skupom `iris.csv`

## Zvanična dokumentacija

* NumPy: [https://numpy.org/](https://numpy.org/)
* Pandas: [https://pandas.pydata.org/](https://pandas.pydata.org/)
* Matplotlib: [https://matplotlib.org/](https://matplotlib.org/)
