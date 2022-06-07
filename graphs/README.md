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

## [Top Reviewers](https://matteofasulo.github.io/PyTripAdvisor/graphs/top_roman_reviewers.html)

## Conclusioni
...............
