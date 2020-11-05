Distribuiranost programa sam postigao tako da glsvni proces predaje novim procesima jedan bucket.
Kreirani procesi rade merge sort na dobivenom bucketu te vraćaju ga sortiranog glavnom procesu putem operatora !.
Kreirani procesi znaju PID glavnog procesa jer je predan kao argument kod stvaranja.
Glavni proces nakon kreiranja svih procesa, čiji broj odgovara broju bucketa čeka prvo odgovor od prvog kreiranog bucketa pa drugog sve dok ne dobije odgovor od zadnjeg.
PID-ovi kreiranih procesa se čuvaju u listi te tako glavni proces zna po kojem redosljedu prima odgovore.
