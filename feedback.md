Dzień dobry, mam następujące uwagi do poprawki etapu 1:

+- to nadal nie jest definicja problemu biznesowego, w najlepszym razie to jest definicja zadania biznesowego
+ zdefiniowane zadania modelowania,
+ zdefiniowane analityczne kryterium sukcesu
- nie wiadomo jaką wartość ma mieć alfa - na tym etapie ta wartość powinna być ustalona
+ brak sensownego kryterium biznesowego
+ zdefiniowane dane wejściowe i zmienna celu
* eksploracyjna analiza dostarczonych danych:
  + sprawdzenie wartości błędnych/brakujących.
  + sprawdzenie wstępnej informatywności danych

 

Otrzymujecie Państwo 17 / 20 punktów za etap 1



Dzień dobry, przesyłam swoje uwagi do etapu 2:
a modele
+ model bazowy,
+ model docelowy,
– brak informacji odnośnie strojenia hiperparametrów,
+ porównanie modeli offline,
+ przejrzysta prezentacja wyników,
+ zawarcie całego kodu potrzebnego do przetrenowania modeli,
– dłuższe fragmenty kodu lepiej z notatnika przenieść do modułów pythona – jest wtedy czytelniej i da się z tego samego kodu korzystać w kilku miejscach,

 

b serwis,
+ poprawna forma – usługa, którą dałoby się wdrożyć na środowisko produkcyjne,
+- serwowanie predykcji z przygotowanych modeli jest w złej formie - dlaczego nie zwraca się jsona tylko sformatowany napis?
– brak możliwości przeprowadzenia eksperymentu A/B – mamy dwa osobne endpointy do modeli,
+ zbieranie logów z eksperymentu,
+ stosowanie dobrych praktyk programistycznych,
– w pliku z wymaganymi pakietami dobrze podać konkretne wersje bibliotek,
– brak jakichkolwiek testów automatycznych,
+ przykłady pokazujące, że serwis działa.

 

Otrzymujecie Państwo: 13 + 9 = 21 pkt. za etap 2.