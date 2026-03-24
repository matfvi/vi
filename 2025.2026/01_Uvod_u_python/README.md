# Tematika
- Uvod u VI
    - Bodovanje
    - Primena vestacke inteligencije
- Uvod u Python
    - [Jupyter notebook](https://jupyter.org/)
    - Podsecanje na osnovne Python-a
    - OOP koncepti u Python-u

## Uvod u VI

### Primena vestacke inteligencije

#### 1. Informisano pretrazivanje (Informed search)
- [Dijkstra vs A* vs Concurrent Dijstra](https://www.youtube.com/watch?v=cSxnOm5aceA) — primeri heuristika i prioriteta.
- [A* vs Dijkstra](https://www.youtube.com/watch?v=g024lzsknDo) — vizualizacija rada heuristike u grafovima.
- [Pathfinding algorithms in Java](https://www.youtube.com/watch?v=CLbqqb53DLA&app=desktop) — implementacije A*, BFS i dijametralnih heuristika.
- [Jump Point Search+](https://www.gdcvault.com/play/1022094/JPS-Over-100x-Faster-than) — optimizovana verzija A* koja preskace nepotrebne cvorove.
- [Ant optimization](https://www.youtube.com/watch?v=eVKAIufSrHs) i [Particle swarm optimization](https://www.youtube.com/watch?v=gkGa6WZpcQg) — metaheuristike za rasporede i optimizaciju.

#### 2. Logika i SAT/SMT
- [Coloring graph using SAT](https://www.youtube.com/watch?v=0gt503wK7AI&t=194s) — modelovanje problema bojenja u CNF.
- [Resavanje Sudoku koristeci SAT](https://github.com/lakshayg/sudoku) — primer kako SMT solver `z3` fiksira ogranicenja.
- [Cleverbot](http://www.cleverbot.com/) — primer jednostavne provere logickih odgovora bazirane na istoriji konverzacije.

#### 3. Supervised learning
- [Stanford CS231n lecture playlist](https://www.youtube.com/playlist?list=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv) — konvolutivne mreze i klasifikacija.
- [Uczimo Python blog: Supervised Learning Tutorials](https://towardsdatascience.com/tagged/supervised-learning) — kratki vodiči sa kod primerima.
- [Kaggle intro to Machine Learning](https://www.kaggle.com/learn/intro-to-machine-learning) — hands-on vodič sa dataset-ovima.

#### 4. Unsupervised learning
- [Distill.pub: Dimensionality reduction visualization](https://distill.pub/2016/misread-tsne/) — vizualni uvid u t-SNE.
- [Google research blog: Clustering and representation learning](https://research.googleblog.com/2017/05/unsupervised-learning-without-labels.html) — transformer u unsupervisedu.
- [Uczimo Python blog: Autoencoders i klasterovanje](https://towardsdatascience.com/autoencoders-for-unsupervised-learning-9f32b70b4003).

#### 5. Reinforcement learning
- [DeepMind Parkour](https://www.youtube.com/watch?v=g59nSURxYgk) — RL agenti u kompleksnim okruzenjima.
- [AI igra Marija](https://www.youtube.com/watch?v=A97HL3_fxyo) i [AI learns to play snake](https://www.youtube.com/watch?v=3bhP7zulFfY) — Q-learning i policy optimization.
- [AI learns to drive in GTA V](https://www.youtube.com/watch?v=edWI4ZnWUGg) — kontrola vozila sa RL.
- [AI learns to play 2048](https://www.youtube.com/watch?v=JQut67u8LIg) — primena Monte Carlo Tree Search kao kombinovane strategije.

#### 6. LLM / GPT / kodiranje
- [OpenAI blog: GPT-4 Technical Report](https://openai.com/research/gpt-4) — arhitektura i aplikacije LLM-a.
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — originalni transformer paper.
- [Hugging Face course](https://huggingface.co/learn/nlp-course/) — prakticno kodiranje i rad sa encoder/decoder modelima.
- [OpenAI Cookbook: Prompt engineering](https://github.com/openai/openai-cookbook) — primeri promptova, API poziva i kod generacije.

### Instalacija Jupyter okruženja

Jupyter je open-source veb aplikacija koja omogucava interaktivno pisanje i pokretanje Python koda.
Preporuka je da se koristi virtuelno okruzenje.

Na Ubuntu sistemu:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip
```

Kreiranje i aktivacija virtuelnog okruzenja:
```bash
python3 -m venv venv
source venv/bin/activate
```

Instalacija JupyterLab:
```bash
python -m pip install --upgrade pip
python -m pip install jupyterlab
```

Provera verzije Python-a:
```bash
python --version
```

Pokretanje JupyterLab servera:
```bash
mkdir -p ~/matf/vi/2025.2026
cd ~/matf/vi/2025.2026
jupyter lab
```

Server ce biti dostupan na adresi prikazanoj u terminalu (najcesce `http://localhost:8888`).
