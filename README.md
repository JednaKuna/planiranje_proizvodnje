# planiranje_proizvodnje

Aplikacija za planiranje serijske proizvodnje

Za izračun optimalne proizvodnje koristimo Wagner-Within metodu

Ulazne vrijednosti su:

        1. trošak pripreme linije
        2. trošak skladištenja po jedinici vremena
        3. prognoza za količinu po jedinici vremena
        4. jedinica vremena
        5. trošak proizvodnje po komadu

Za određivanje broja serija koristim Wagner-Within metodu za koju su potrebni svi gore navedeni podatci osim troškova proizvodnje.
Troškove skladištenja ne računam za komade koje šaljem van taj mjesec nego samo za one koji se šalju van u narednim mjesecima.

Nakon što izračunam najbolji raspored serija onda dodam i troškove proizvodnje kako bi prikazao učinkovitost tog 'optimalnog' načina proizvodnje.

Wagner-Whitin metoda

Prednosti:
Optimalno rješenje za determinističke uvjete, Minimizacija ukupnih troškova, Fleksibilnost za promjenjive potražnje u slučaju da je potražnja poznata, Jednostavnost implementacije, Koristi princip dinamičkog programiranja

Nedostatci:
Pretpostavka determinističkih uvjeta, Ograničenost vremenskog horizonta, Neefikasnost kod velikih problema, Ne uzima u obzir stohastičku potražnju, Ne uzima u obzir kapacitetska ograničenja, Osjetljivost na promjene ulaznih podataka

Kada koristiti?
Kada imate dobro definiranu i predvidivu potražnju.
Kad je problem relativno jednostavan i odnosi se na optimizaciju troškova u pojedinom skladištu ili proizvodnom procesu.
Ako nema značajnih kapacitetskih ograničenja ili nesigurnosti.
