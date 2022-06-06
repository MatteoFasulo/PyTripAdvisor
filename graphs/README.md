# Graphs
## [Sunburst](https://matteofasulo.github.io/PyTripAdvisor/graphs/sunburst.html)
Attraverso il `sunburst` abbiamo rappresentato la distribuzione dei voti attribuiti alle recensioni e le loro relative fasce di prezzo corrispettive. Abbiamo notato che:
* La maggior parte delle recensioni rientra nella fascia di prezzo `4 - 4.5` con predominanza dei ristoranti in fascia di prezzo media. La categoria dei ristoranti con 5 stelle, invece, presenta ugual numero di ristoranti di fascia economica e media. 

## [Rating per Price](https://matteofasulo.github.io/PyTripAdvisor/graphs/avg_rating_per_price.html)
La rappresentazione della fascia di prezzo del ristorante in funzione del numero medio di recensioni aiuta a comprendere in media quando si scrive una recensione. Dividendo le diverse fasce di prezzo ognuna a seconda del rating della recensione scopriamo che:
* Nei ristoranti economici in media si scrivono recensioni più positive che negative.
* Nei ristoranti di fascia media si scrive molto di più quando si è particolarmente entusiasti dell'esperienza.
* Nei ristoranti costosi si scrive quando si è molto insoddisfatti del ristorante.
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
L'analisi prosegue con lo studio dei diversi tipi di cucina di ogni ristorante di Roma. Visto che la maggior parte dei ristoranti ha come tipologia di cucina primaria quella `italiana` abbiamo scelto come tipo di cucina primario quello immediatamente successivo così da considerare il secondo tipo di cucina caratteristica di ogni ristorante. Selezionando poi i primi 10 tipi di cucina abbiamo notato che:
* La cucina giapponese non è molto apprezzata
* Un'altissima percentuale di ristoranti ha come tipologia di cucina la pizza ma questa non rappresenta la categoria maggiormente apprezzata
* I ristoranti di **pesce** hanno in media un rating più elevato rispetto a qualunque altra categoria di cucina seguita da quella **mediterranea**

## [Diet Types](https://matteofasulo.github.io/PyTripAdvisor/graphs/diet_types.html)
Durante la fase di scraping abbiamo preso anche l'informazione sulle diete particolari come:
* Ristoranti con opzioni vegetariane
* Ristoranti con opzioni vegane
* Ristoranti gluten-free

I 3 `scatterplot` mostrano le percentuali di disponibilità delle diete particolari stratificati per municipio. Possiamo vedere come il [Municipio I](https://it.wikipedia.org/wiki/Municipio_Roma_I) sia sempre in cima per percentuale di ristoranti con diete particolari mentre il [Municipio VI](https://it.wikipedia.org/wiki/Municipio_Roma_VI) è sempre posizionato tra gli ultimi posti.
> **Info:** Il [Municipio XIV](https://it.wikipedia.org/wiki/Municipio_Roma_XIV) ha un punto percentuale in più di ristoranti con opzioni vegetariane rispetto al [Municipio I](https://it.wikipedia.org/wiki/Municipio_Roma_I). 

## Conclusioni
...............
