# FAQ
## Jak to włączyć?
Aby włączyć naszą implementacje modeli należy mieć pobranego Python 3.10+ z bibliotekami z pliku reqirements.txt

python3 main.py

mikroserwis działa na localhost:8000

## Jak to działa?

Możemy serwować predykcje dla wszystkich artystów odnośnie których dostaliśmy dane, pełna lista artystów znajduje się w pliku artists.txt

Wykresy z predykcjami na następny rok znajdują się na:

http://localhost:8000/predict_plot/[artist_name]

dla przykłądowego artysty "XXXTENTACION" będzie to

http://localhost:8000/predict_plot/XXXTENTACION

mamy dostęp do 2 modeli:
- arima
- naive

Predykcje na następny miesiąc wyrażone w procentach znajdują się na:

http://localhost:8000/predict/[model_name]/[artist_name]

Przykładowa predykcja dla artysty XXXTENTACION:

http://localhost:8000/predict/arima/XXXTENTACION

http://localhost:8000/predict/naive/XXXTENTACION

Predykcje zapisywane są w pliku ab_test_data.json, dostęp do pliku przez stronę:

http://localhost:8000/test_ab

## Uwagi

nie wszystkie bloki kodu z Etap1 mogą działać, gdyż chcemy ograniczyć wysłane dane do minimum
