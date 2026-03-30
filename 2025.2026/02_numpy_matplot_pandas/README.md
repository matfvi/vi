
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

---

## 4. Najčešće korišćene `NumPy` funkcije

1. `np.array(object, dtype=None, copy=True)`
   Kreira `ndarray` iz liste, tuple-a ili drugog iterabilnog objekta.

2. `np.asarray(a, dtype=None)`
   Pretvara postojeći objekat u `ndarray`, često bez dodatnog kopiranja podataka.

3. `np.arange([start,] stop[, step], dtype=None)`
   Generiše niz ravnomerno raspoređenih vrednosti sa zadatim korakom.

4. `np.linspace(start, stop, num=50, endpoint=True)`
   Generiše zadat broj tačaka između dve granične vrednosti.

5. `np.zeros(shape, dtype=float)`
   Kreira niz zadatog oblika čiji su svi elementi nule.

6. `np.ones(shape, dtype=float)`
   Kreira niz zadatog oblika čiji su svi elementi jedinice.

7. `np.full(shape, fill_value, dtype=None)`
   Kreira niz popunjen jednom istom vrednošću.

8. `np.eye(N, M=None, k=0, dtype=float)`
   Kreira jediničnu matricu.

9. `np.reshape(a, newshape)`
   Menja oblik niza bez promene njegovih vrednosti.

10. `np.ravel(a, order='C')`
    Pretvara višedimenzioni niz u jednodimenzioni prikaz.

11. `np.transpose(a, axes=None)`
    Menja raspored osa niza.

12. `np.concatenate((a1, a2, ...), axis=0)`
    Spaja više nizova duž postojeće ose.

13. `np.stack(arrays, axis=0)`
    Spaja više nizova tako što uvodi novu osu.

14. `np.sum(a, axis=None)`
    Računa zbir elemenata niza.

15. `np.mean(a, axis=None)`
    Računa aritmetičku sredinu elemenata niza.

16. `np.std(a, axis=None)`
    Računa standardnu devijaciju elemenata niza.

17. `np.min(a, axis=None)`
    Vraća minimalnu vrednost u nizu ili duž zadate ose.

18. `np.max(a, axis=None)`
    Vraća maksimalnu vrednost u nizu ili duž zadate ose.

19. `np.argmax(a, axis=None)`
    Vraća indeks najvećeg elementa.

20. `np.where(condition, [x, y])`
    Bira elemente uslovno ili vraća indekse gde je uslov ispunjen.

## 5. Najčešće korišćene `Pandas` funkcije

1. `pd.read_csv(filepath_or_buffer, sep=',', ...)`
   Učitava CSV fajl u `DataFrame`.

2. `pd.DataFrame(data=None, index=None, columns=None)`
   Kreira tabelu iz rečnika, liste ili drugog izvora podataka.

3. `df.head(n=5)`
   Prikazuje prvih `n` redova tabele.

4. `df.info()`
   Ispisuje osnovne informacije o kolonama, tipovima i nedostajućim vrednostima.

5. `df.describe()`
   Računa osnovne statistike za numeričke kolone.

6. `df.copy(deep=True)`
   Pravi kopiju `DataFrame` objekta.

7. `df.dropna(axis=0, how='any')`
   Uklanja redove ili kolone sa nedostajućim vrednostima.

8. `df.fillna(value)`
   Popunjava nedostajuće vrednosti zadatom vrednošću ili pravilom.

9. `df.astype(dtype)`
   Menja tip podataka u kolonama.

10. `df.rename(columns=None, index=None)`
    Menja nazive kolona ili indeksa.

11. `df.drop(labels=None, axis=0)`
    Uklanja redove ili kolone po nazivu.

12. `df.loc[row_labels, col_labels]`
    Bira redove i kolone po oznakama.

13. `df.iloc[row_positions, col_positions]`
    Bira redove i kolone po pozicijama.

14. `df.sort_values(by, ascending=True)`
    Sortira tabelu po jednoj ili više kolona.

15. `df.groupby(by)`
    Grupiše podatke radi agregacije i analize.

16. `df.value_counts()`
    Broji pojavljivanja vrednosti.

17. `df.unique()`
    Vraća jedinstvene vrednosti iz `Series` objekta.

18. `df.apply(func, axis=0)`
    Primenjuje funkciju nad kolonama ili redovima.

19. `pd.merge(left, right, on=None, how='inner')`
    Spaja dve tabele po zajedničkom ključu.

20. `df.reset_index(drop=False)`
    Resetuje indeks tabele.

## 6. Najčešće korišćene `Matplotlib` funkcije

1. `plt.figure(figsize=None)`
   Kreira novu figuru.

2. `plt.subplots(nrows=1, ncols=1, figsize=None)`
   Kreira figuru i jednu ili više osa.

3. `plt.plot(x, y, label=None, ...)`
   Crta linijski grafik.

4. `plt.scatter(x, y, c=None, ...)`
   Crta tačkasti grafik.

5. `plt.bar(x, height, ...)`
   Crta stubičasti grafik.

6. `plt.hist(x, bins=None, ...)`
   Crta histogram.

7. `plt.imshow(X, cmap=None, ...)`
   Prikazuje matricu ili sliku.

8. `plt.title(label)`
   Postavlja naslov grafikona.

9. `plt.xlabel(xlabel)`
   Postavlja oznaku x-ose.

10. `plt.ylabel(ylabel)`
    Postavlja oznaku y-ose.

11. `plt.legend()`
    Prikazuje legendu.

12. `plt.grid(visible=True, ...)`
    Uključuje pomoćnu mrežu.

13. `plt.xlim(left=None, right=None)`
    Podešava opseg x-ose.

14. `plt.ylim(bottom=None, top=None)`
    Podešava opseg y-ose.

15. `plt.xticks(ticks=None, labels=None)`
    Podešava pozicije i natpise na x-osi.

16. `plt.yticks(ticks=None, labels=None)`
    Podešava pozicije i natpise na y-osi.

17. `plt.tight_layout()`
    Automatski sređuje razmak između elemenata figure.

18. `plt.style.use(style)`
    Menja globalni vizuelni stil grafikona.

19. `plt.savefig(fname, dpi=None, bbox_inches=None)`
    Čuva grafikon u fajl.

20. `plt.show()`
    Prikazuje gotov grafikon na ekranu.
