`agent.py` pokazuje najvažniju ideju modernih agenata za kodiranje: model ne menja fajlove sam, već predlaže sledeći korak, a agent.py taj korak izvršava kroz ograničen skup alata.

Ovo je uvodni primer za studente. Cilj je razumeti principe sistema kao što su Claude Code, Codex i slični agenti.

## Glavna ideja

Coding agent je petlja.

U svakoj iteraciji dešava se sledeće:

1. Programom agent.py dajemo zadatak agentu pomoću prompta.
2. Model odlučuje da li treba da koristi alat.
3. Program proverava odgovor modela i izvršava traženi alat.
4. Rezultat alata se vraća modelu kao novi kontekst.
5. Model nastavlja dok ne pošalje završni odgovor.

Većina "inteligencije" dolazi iz modela, dok Python kod daje modelu ruke: pregled fajlova, čitanje fajlova i upisivanje izmena.

## Implementacija

LLM nije operativni sistem. Model ne vidi naš disk, ne zna šta je u projektu i ne može sam da pokrene izmenu fajla. On samo generiše tekst. Ako želimo da taj tekst postane akcija, naš program mora da definiše pravila: koje komande postoje, kako izgledaju i šta se radi sa njihovim rezultatom.

Alati su neka vrsta komunikacionog protokola između modela i programa. U `agent.py`, model mora da odgovori JSON objektom. Ako želi da vidi projekat, traži `list_files`. Ako želi sadržaj, traži `read_files`. Ako želi izmenu, traži `edit_files`.

Posle svake akcije, rezultat se dodaje u trenutni razgovor. To je razlog zašto i mali agent može da reši zadatke koji traže više koraka.

## Petlja izvršavanja

`agent.py` možemo zamisliti kao prevodioca između OS i LLM-a. Program stoji između OS i LLM-a, promptove šalje LLM-u, koji generiše komande koje program treba da izvrši. Program izvršava komande LLM-a i rezultat izvršavanja komandi šalje nazad LLM-u.

## Kako ga pokrenuti

Primer koristi lokalni Ollama server i model naveden u `MODEL`.

```bash
python3 agent.py
``
```
