# Vežbe 10 - Neuronske mreže

<img alt="nn" src="https://www.astroml.org/_images/fig_neural_network_1.png">

## Materijali

- `01_tf_keras_fashion_mnist.ipynb` - primer sa klasifikacijom nad skupom `Fashion MNIST`
- `01_tf_keras_fashion_mnist.html` - sveska u `html` formatu
- `01.neural.network.diagram.svg` - dijagram modela
- `02_tf_keras_fuel.ipynb` - primer sa regresijom nad skupom `Auto MPG`
- `02_tf_keras_fuel.html` - sveska u `html` formatu
- `02.neural.network.diagram.svg` - dijagram modela

Snimak sa časa: [ovde](https://www.youtube.com/watch?v=pNwMY9Xxm_M).

## Alat *Neural Network Playground*

Na [ovoj](https://playground.tensorflow.org/) adresi možete pronaći alat Neural Network Playground
koji ima izuzetno lepu vizuelizaciju neuronskih mreža. Poigrajte se malo sa funkcionalnostima
i produbite vaše razumevanje neuronskih mreža.

## Kako pokrenuti

### Google Collab

Za pokretanje i rad se predlaže korišćenje platforme Google Collab koja nudi virtuelnu
mašinu na kojoj je podešeno okruženje za rad inpirisano Jupyter Notebook sveskama.

Najbolje je da na Vašem Google Drive nalogu napravite lepu strukturu direktorijuma
za rad u okviru kursa, na primer:

```
matf
└── vi
    └── materijali_sa_vezbi
        └── 10.neuronske.mreze
            └── tf_keras_fashion_mnist.ipynb
            └── tf_keras_fuel.ipynb
```

i da `ipynb` datoteke pokrećete iz platforme Google Drive putem Google Collab aplikacije.
Osim toga, možete direktno da učitate te datoteke kroz Google Collab (File -> Upload Notebook).

Google Collab pruža grafičko karticu u okruženju za rad:
```
Runtime
└── Change runtime type
    └── Hardware accelerator
        └── GPU
```

### Lokalno na računaru

Ukoliko želite da pokrenete lokalno na računaru biće vam neophodne biblioteke:

- `tensorflow` ili `tensorflow-gpu` (>= 2.0)
- `numpy`
- `pandas`
- `seaborn`
- `matplotlib`
- `jupyterlab`

#### Virtuelno okruženje

Savetuje se da biblioteke instalirate u virtuelno okruženje umesto direktno na sistem.
Da bi napravili virtuelno okruženje sa imenom `venv` možete da uradite:

```
python -m venv venv
```

Potom je potrebno da ga aktivirate.

```
source venv/bin/activate
```

U konzoli će vam se pojaviti oznaka da je virtuelno okruženje aktivno. Najčešće je to tekst
`(venv)` negde u konzoli. Više o virtuelnim okruženjima [ovde](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### Instalacija biblioteka

Nakon što je virtuelno okruženje aktivno, možemo preći na instalaciju potrebnih biblioteka.

```
pip install seaborn numpy pandas jupyterlab matplotlib
```

Alat `pip` će preuzeti i instalirati navedene biblioteke u virtuelno okruženje koje smo
prethodno napravili. Slobodni ste da instalirate i druge dodatne biblioteke.

#### Biblioteka `tensorflow`

Biblioteka tensorflow je dostupna kroz pakete:
- `tensorflow` - izračunavanje se vrši na procesoru
- `tensorflow-gpu` - izračunavanje ima podršku za rad na grafičkoj kartici

Na kursu ćemo koristiti tensorflow 2.0 i novije varijante. Biblioteka
`keras` dolazi instalirana u okviru biblioteke `tensorflow`, ali je **važno**
da je u pitanju verzija barem 2.0!

Osim toga, ukoliko ne želite podršku za izračunavanje na grafičkoj kartici,
možete `tensorflow` instalirati slično kao prethodne biblioteke sa:

```
pip install tensorflow
```

Ako želite da navede koju tačno verziju hoćete onda:

```
pip install tensorflow==2.0
```

Ako **želite** podršku za izračunavanje na grafičkoj kartici, trebaće vam CUDA na sistemu.
Instalacije CUDA paketa varira od sistema do sistema, kao i od distribucije do distribucije
pa za upustva možete pogledati na internetu u zavisnosti od vaše situacije.

Važno je da vaša grafička kartica podržava verziju paketa CUDA koji zahteva `tensorflow-gpu`
paket koji želite da instalirate.

Zvanična `tensorflow` [upustva](https://www.tensorflow.org/install/gpu).
