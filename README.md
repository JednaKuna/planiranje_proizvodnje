# planiranje_proizvodnje

Aplikacija za planiranje serijske proizvodnje

Za izračun optimalne proizvodnje koristimo Wagner-Within metodu u kombinaciji sa Stohastičkim modeliranjem nesigurnosti

Ulazne vrijednosti su:

        1. trošak pripreme linije
        2. trošak skladištenja po jedinici vremena
        3. prognoza za količinu po jedinici vremena
        4. jedinica vremena
        5. trošak proizvodnje po komadu
        6. service level (%)
        7. standardna devijacija
        8. offset devijacije
        9. broj scenarija za simulaciju

Za određivanje broja serija koristim Wagner-Within metodu.

Wagner-Whitin metoda

Prednosti:
Optimalno rješenje za determinističke uvjete, Minimizacija ukupnih troškova, Fleksibilnost za promjenjive potražnje u slučaju da je potražnja poznata, Jednostavnost implementacije, Koristi princip dinamičkog programiranja

Nedostatci:
Pretpostavka determinističkih uvjeta, Ograničenost vremenskog horizonta, Neefikasnost kod velikih problema, Ne uzima u obzir stohastičku potražnju, Ne uzima u obzir kapacitetska ograničenja, Osjetljivost na promjene ulaznih podataka

Kada koristiti?
Kada imate dobro definiranu i predvidivu potražnju.
Kad je problem relativno jednostavan i odnosi se na optimizaciju troškova u pojedinom skladištu ili proizvodnom procesu.
Ako nema značajnih kapacitetskih ograničenja ili nesigurnosti.

Kombiniranje stohastičkog modeliranja s Wagner-Whitin metodom

        Kombinacija ovih pristupa može pomoći u suočavanju s nesigurnostima, primjerice u potražnji ili troškovima.
        Za ovaj primjer smo uzeli u obzir nesigurnosti u potražnji.

        Ovo su koraci:
        1. Identifikacija nesigurnosti: Odredimo koji aspekti Wagner-Whitin modela nisu sigurni (potražnja).
        2. Modeliranje nesigurnosti: Koristimo stohastičke varijable za opisivanje nesigurnih parametara(Normalna distribucija).
        3. Generiranje scenarija: Koristimo Monte Carlo simulaciju pomoću koje stvaramo velik boj mogućih scenarija
        4. Primjena Wagner-Whitin metode: Za svaki scenarij, primijenimo Wagner-Whitin algoritam kako bi izračunali optimalni plan zaliha i proizvodnje.
        5. Evaluacija rezultata: Analiziramo rezultate svih scenarija kako bi identificirali trendove, rizike i očekivane troškove.
