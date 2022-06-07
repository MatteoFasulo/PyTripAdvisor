# Graphs
## [Sunburst](https://matteofasulo.github.io/PyTripAdvisor/graphs/sunburst.html)
Attraverso il `sunburst` abbiamo rappresentato la distribuzione della media dei voti delle recensioni e la loro relativa fascia di prezzo. Abbiamo notato che:
* la maggior parte dei ristoranti rientra nella fascia di recensioni `4 - 4.5 stelle` con predominanza di quelli nella fascia media di prezzo. La categoria dei ristoranti con `5 stelle`, invece, presenta una differenza minima tra il numero di ristoranti nella fascia economica e media. 

## [Rating per Price](https://matteofasulo.github.io/PyTripAdvisor/graphs/avg_rating_per_price.html)
La rappresentazione della fascia di prezzo del ristorante in funzione del numero medio dei voti delle recensioni permette di visualizzare in media quando viene lasciata una recensione. Analizzando separatamente le diverse fasce di prezzo ripartite per rating medio della recensione, possiamo notare che:
* nei ristoranti economici in media si scrivono recensioni più positive che negative;
* nei ristoranti di fascia media si scrivono molte più recensioni quando si è particolarmente entusiasti dell'esperienza;
* nei ristoranti costosi vengono lasciate recensioni in particolare quando i clienti sono molto insoddisfatti della proposta del ristorante.
  > **Info:** In media si scrive **4** volte di più quando si è insoddisfatti per via del costo elevato del ristorante

## [Restaurant Count](https://matteofasulo.github.io/PyTripAdvisor/graphs/count_restaurants_by_municipio.html)
Il `barplot` del numero dei ristoranti stratificato per municipio evidenzia come la maggior parte dei ristoranti si trovi al centro di Roma (zona [Municipio I](https://it.wikipedia.org/wiki/Municipio_Roma_I)) con oltre 2.7k ristoranti mentre la seconda zona è rappresentata del [Municipio II](https://it.wikipedia.org/wiki/Municipio_Roma_II) con oltre 800 ristoranti.
* Il [Municipio II](https://it.wikipedia.org/wiki/Municipio_Roma_II) comprende:
  * Parioli
  * Flaminio
  * San Lorenzo
  * Università
  * Nomentanto
  * Villaggio Olimpico
> **Info:** La zona con minor numero di ristoranti è il [Municipio VI](https://it.wikipedia.org/wiki/Municipio_Roma_VI)

## [TreeMap Restaurants / Municipi](https://matteofasulo.github.io/PyTripAdvisor/graphs/treemap_municipi.html)
Nella `treemap` abbiamo riassunto sia il numero di ristoranti per municipio che il rating medio di ogni zona. Nella treemap maggiore è il numero di recensioni e più grande sarà il riquadro che conterrà la zona; più alto è il valore medio di rating e più chiaro sarà il colore del riquadro.
* Il [Municipio V](https://it.wikipedia.org/wiki/Municipio_Roma_V) ha il rating medio più alto.
* Il [Municipio IX](https://it.wikipedia.org/wiki/Municipio_Roma_IX) ha il rating medio più basso.
* Il [Municipio I](https://it.wikipedia.org/wiki/Municipio_Roma_I) nonostante fosse quello col maggior numero di recensioni, si posiziona a metà nel rating medio tra tutte le zone. 

## [Cuisine Types](https://matteofasulo.github.io/PyTripAdvisor/graphs/cuisine_types.html)
L'analisi prosegue con lo studio dei diversi tipi di cucina di ogni ristorante di Roma. Dal momento che la maggior parte dei ristoranti ha come tipologia di cucina primaria quella `italiana`, abbiamo spostato l'attenzione sulla seconda, considerando quest'ultima come punto di partenza per l'analisi. Selezionando, poi, i primi 10 tipi di cucina abbiamo notato che:
* la cucina giapponese non è molto apprezzata;
* un'altissima percentuale di ristoranti ha come tipologia di cucina la pizza ma questa non rappresenta la categoria maggiormente apprezzata;
* i ristoranti di **pesce** hanno, in media, un rating più elevato rispetto a qualunque altra categoria di cucina, seguiti da quelli **mediterranei**.

## [Diet Types](https://matteofasulo.github.io/PyTripAdvisor/graphs/diet_types.html)
Durante la fase di scraping abbiamo scaricato anche l'informazione sulle "restrizioni alimentari" come:
* ristoranti con opzioni vegetariane;
* ristoranti con opzioni vegane;
* ristoranti gluten-free.

I 3 `scatterplot` mostrano le percentuali di disponibilità delle diete particolari stratificati per municipio. Possiamo vedere come il [Municipio I](https://it.wikipedia.org/wiki/Municipio_Roma_I) sia sempre in cima per percentuale di ristoranti con diete particolari mentre il [Municipio VI](https://it.wikipedia.org/wiki/Municipio_Roma_VI) è sempre posizionato tra gli ultimi posti.
> **Info:** Il [Municipio XIV](https://it.wikipedia.org/wiki/Municipio_Roma_XIV) ha un punto percentuale in più di ristoranti con opzioni vegetariane rispetto al [Municipio I](https://it.wikipedia.org/wiki/Municipio_Roma_I).  

## [Top Words](https://matteofasulo.github.io/PyTripAdvisor/graphs/hist_top_words.html)
Per l'analisi delle 20 parole più ricorrenti, abbiamo creato un istogramma a partire da un dizionario di conteggi. Quest'ultimo è stato realizzato tokenizzando i testi delle recensioni di tutti i ristoranti, rimuovendo segni di punteggiatura e stopwords. Il grafico ci mostra come la parole più frequente è `molto` seguita da `locale` e `qualità` fino ad arrivare a `buona`.

<img src="[markdownmonstericon.png](https://matteofasulo.github.io/PyTripAdvisor/img/burger_50-1000.png)" alt="Markdown Monster icon" style="float: left; margin-right: 10px;" />

* wordcloud parole più frequenti delle recensioni di tutte le recensioni
* <img src="(https://github.com/MatteoFasulo/PyTripAdvisor/img/food_all.html)"
     alt="food_all"
     style="float: left; margin-right: 10px;" />
* wordcloud parole più frequenti delle recensioni dei ristoranti con recensioni < 50 (pizza)
* wordcloud parole più frequenti delle recensioni dei ristoranti con 50 < recensioni < 1000 (panino)
* wordcloud parole più frequenti delle recensioni dei ristoranti con recensioni > 1000 (frutta)

## [Top Reviewers](https://matteofasulo.github.io/PyTripAdvisor/graphs/top_roman_reviewers.html)
Un'ulteriore considerazione è stata applicata ai dati inerenti i recensori. Lo scatterplot mostra in particolare due recensori dalle caratteristiche completamente opposte:
* il primo presenta un elevato numero di città in cui ha lasciato almeno una recensione, infatti, la percentuale delle recensioni su ristoranti romani è circa del 0.6%, inoltre gli altri utenti non le ritengono utili;
* il secondo presenta, invece, elevata percentuale di recensioni sui ristoranti romani, infatti vi è un minor numero di città visitate e in generale le sue recensioni sono state maggiormente apprezzate.

## Conclusioni
In conclusione possiamo quindi dedurre che, nonostante la fascia più apprezzata sia quella **media**, il cliente ritiene comunque importante la **qualità** del **servizio**. Il suggerimento è quello di aprire un ristorante di qualità con un prezzo medio nella zona del [Municipio IX](https://it.wikipedia.org/wiki/Municipio_Roma_IX) con tipologia di cucina **pesce** e **mediterranea** proponendo diete **vegane** e **senza glutine**.
