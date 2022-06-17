# PyTripAdvisor
## Ristoranti
L’obiettivo del progetto è quello di proporre un’analisi sulle caratteristiche principali dei ristoranti
di Roma, servendosi delle recensioni lasciate dai clienti sul sito web di TripAdvisor. Quest’ultimo
presenta i nomi e le informazioni di 30 ristoranti su ogni pagina contenenti a loro volta 10 recensioni
per foglio. Vogliamo studiare la distribuzione dei ristoranti sul territorio romano, tenendo conto
di:
* informazioni sui ristoranti
  * link ristorante
  * nome
  * rating medio 
  * totale recensioni
  * fascia di prezzo
  * tipo di cucina
  * diete particolari
  * indirizzo

* informazioni sul recensore
  * username
  * link del profilo
  * recensioni totali scritte
  * livello del recensore
  * data di registrazione
  * località di residenza
  * totale città recensite
  * totale voti utili ricevuti

* informazioni sulle recensioni
  * link recensione
  * link ristorante
  * username del recensore
  * titolo
  * data della recensione
  * data di visita del ristorante
  * voto della recensione
  * voti utili ricevuti
  * dispositivo con cui è stata scritta la recensione
  * testo della recensione

### Report
La relazione è disponbilie al seguente [indirizzo](https://github.com/MatteoFasulo/PyTripAdvisor/blob/main/PyTripAdvisor_Report.pdf)

### PyTripAdvisor Class
`PyTripAdvisor`:
* user_exist -> SQL query per verificare la presenza di un utente già memorizzato nella base dati
* restaurant_exist -> SQL query per verificare la presenza di un ristorante già memorizzato nella base dati
* review_exist -> SQL query per verificare la presenza di un recensore già memorizzato nella base dati
* getDriver -> Session del Chromedriver di `Selenium` con opzioni personalizzate
* getRestaurants -> Inserimento nel database di una pagina di ristoranti a partire dal link inserito
* getReviews -> Inserimento nel database delle ultime 200 recensioni a partire dal link del ristorante
* tokenize -> `NLTK` tokenizzazione del testo delle recensioni con rimozione di punteggiatura e stopwords
* wordcloud -> Rappresentazione grafica delle parole più frequenti con diverse maschere

### Maps
* [Distribuzione dei ristoranti](https://matteofasulo.github.io/PyTripAdvisor/map/mappa.html)
> **Tip:** E' possibile selezionare le singole fasce di prezzo (Cheap, Reasonable, Expensive) dal menù in alto a destra nella mappa

### Dataset
- Il dataset è memorizzato nel database SQL 'ristoranti_sql.gz' compressa in *gzip* e successivamente diviso in parti di dimensioni minori di 25MB per poter essere caricato su GitHub;
> **Ripristino (MySQL):** 
> 
> $ cat ristoranti_sql.gz.part-* > ristoranti_sql.gz
> 
> $ gunzip < 'ristoranti_sql.gz' | mysql -u [user] -p[pass]


### Libraries

| Name | Description |
| ------------- | ------------------------------ |
| [Numpy] | package for scientific computing with Python.
| [Pandas]| fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.
| [Folium]| folium builds on the data wrangling strengths of the Python ecosystem and the mapping strengths of the Leaflet.js library.
| [Os]| this module provides a portable way of using operating system dependent functionality.
| [Json]| the json library can parse JSON from strings or files.
| [Math]| access to the mathematical functions defined by the C standard.
| [Random]| pseudo-random number generators for various distributions.
| [Matplotlib]| library for creating static, animated, and interactive visualizations in Python.
| [Plotly]| graphing library makes interactive, publication-quality graphs.
| [Regex]| regular expression matching operations similar to those found in Perl.
| [Selenium]| API to write functional/acceptance tests using Selenium WebDriver.
| [BeautifulSoup]| library for pulling data out of HTML and XML files.
| [MySQL]| MySQL connector for python.
| [WordCloud]| word cloud generator in Python.

[os]: <https://docs.python.org/3/library/os.html>
[json]: <https://docs.python.org/3/library/json.html>
[Numpy]: <https://numpy.org/install/>
[Pandas]: <https://pandas.pydata.org/>
[Folium]: <https://python-visualization.github.io/folium/>
[Math]: <https://docs.python.org/3/library/math.html>
[Random]: <https://docs.python.org/3/library/random.html>
[NetworkX]: <https://networkx.org/>
[PowerLaw]: <https://pypi.org/project/powerlaw/>
[EmpiricalDist]: <https://pypi.org/project/empiricaldist/>
[Matplotlib]: <https://matplotlib.org/>
[Plotly]: <https://plotly.com/python/>
[Kaleido]: <https://pypi.org/project/kaleido/>
[MPL Toolkits]: <https://matplotlib.org/stable/tutorials/toolkits/mplot3d.html>
[Regex]: <https://docs.python.org/3/library/re.html>
[Selenium]: <https://selenium-python.readthedocs.io/>
[BeautifulSoup]: <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
[MySQL]: <https://dev.mysql.com/doc/connector-python/en/>
[WordCloud]: <https://pypi.org/project/wordcloud/>
