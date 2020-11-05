# 3. laboratorijska vježba
# Sigurnost mrežnih protokola i vatrozid

Dohvatite najnoviju verziju zadatka:

```
$ git pull
```

Na virtualnom stroju su postavljena 3 mrežna sučelja:

- NAT
- "Bridged Adapter"
- "Host-only Adapter"

Logirajte se u virtualni stroj i provjerite dodijeljene IP adrese:
```
$ ip addr
...
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s3
...
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 10.19.0.136/24 brd 10.19.0.255 scope global dynamic noprefixroute enp0s8
...
4: enp0s9: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 192.168.56.101/24 brd 192.168.56.255 scope global dynamic noprefixroute enp0s9
```

U prikazanom ispisu je NAT sučelju dodijeljena adresa 10.0.2.15, "Bridged" sučelju adresa 10.19.0.136, a "Host-
only" sučelju adresa 192.168.56.101.

Zadatak se sastoji od 4 dijela. Prva dva dijela izvode se s vašeg računala ("host" na kojem je instaliran VirtualBox).
Kao "vanjsku adresu" vašeg virtualnog stroja možete koristiti adrese "Bridged" ili "Host-only" sučelja.


## 1) Skeniranje alatom ping

NAPOMENA: Ovaj zadatak izvodite na vašem računalu, a ne na virtualnom stroju.

S pomoću naredbe `ping` probajte pingati sljedeća računala:

    1. Vaš virtualni stroj
    2. mail.fer.hr
    3. 161.53.19.1
    4. imunes.net

Proučite povratne TTL vrijednosti koje Vam se ispisuju. Zaključite početne TTL
vrijednosti. Možete li s pomoću tih vrijednosti zaključiti koji je operacijski
sustav trenutno pokrenut na tim računalima? Objasnite.

## 2) Skeniranje alatom nmap

NAPOMENA: Ovaj zadatak izvodite na vašem računalu, a ne na virtualnom stroju.
Prije pokretanja skeniranja, unutar virtualnog stroja pokrenite sljedeću naredbu
koja će vam omogućiti pregled dolaznih veza na virtualni stroj:

```
    $ watch -n 0.5 netstat -ant
```

Vaš zadatak je s pomoću alata `nmap` otkriti trenutno pokrenute servise na
virtualnom stroju. Isprobajte sljedeće opcije u alatu `nmap`:
 - skeniranje TCP i UDP portova
 - TCP syn scan
 - detekcija operacijskog sustava (-O)
 - detekcija verzija servisa (-sV)
 - općeniti scan (-A opcija)

Navedite koji je način skeniranja prouzročio promjenu ispisa na virtualnom
stroju. Objasnite.

Možete na stroju s kojega skenirate pokrenuti alat Wireshark kako bi vidjeli
promet koji alat `nmap` generira.

Usporedite rezultate skeniranja izvana i iznutra:
```
    C:\> nmap -sV _vanjska_adresa_

    sui@sui$ sudo nmap -sV localhost
```

U čemu se ta dva ispisa razlikuju? Objasnite.

## 3) Konfiguracija vatrozida 

Treći dio zadatka izvodi se na virtualnom stroju na kojem se pokrene IMUNES eksperiment.

U datoteci NETWORK.imn nalazi se primjer mreže s demilitariziranom zonom.

Pokrenite IMUNES eksperiment:

```
$ sudo imunes NETWORK.imn
```
Pokretanjem eksperimenta, automatski će se pokrenuti i mreže usluge:
- SSH poslužitelj na FW, FW_int, mail-relay, web i mail,
- HTTP poslužitelj na čvoru web,
- e-mail poslužitelj (SMTP) na čvorovima mail-relay i mail.

![slika mreže](network.png) 

Vaš je zadatak konfigurirati vanjski i unutarnji vatrozid te provjeriti dostupnost usluga iz vanjske mreže (Interneta) i iz lokalne mreže.

Vanjski vatrozid (FW) ima dva sučelja:
- eth0 povezuje mrežu s pružateljem usluga (ISP) i ima statičku adresu 192.0.2.1/24,
- eht1 je interno sučelje prema demilitariziranoj zoni sa statičkom adresom 192.168.2.1/24.

U DMZ se nalaze web poslužitelj (web) i e-mail poslužitelj (mail-relay).

Unutarnji vatrozid (FW_int) nalazi se izmedju DMZ i unutarnje mreže (LAN):
- eth0 ima statičku adresu 192.168.2.2/24,
- eth1 ima statičku adresu 192.168.1.1/24.

U unutarnjoj mreži (LAN) se nalazi e-mail poslužitelj (mail) i dva korisnička računala, int1 i int2.

Unutarnja mreža LAN koristi privatne adrese te je na vatrozidu FW_int konfiguriran NAT:
- sve konekcije iz lokalne mreže (LAN) prema Internetu odlaze s IP adresom sučelja eth0 vatrozida FW_int, 192.168.2.2,
- IP adresa se ne mijenja za konekcije prema računalima u DMZ.
 
Pravila za translaciju adresa na vatrozidu FW_int već su upisana u datoteku FW_int.sh i nije ih potrebno mijenjati.

Definirajte `iptables` pravila na FW i FW_int u skladu sa sljedećim zahtjevima:

- računala iz lokalne mreže LAN imaju neograničeni pristup poslužiteljima u DMZ i Internetu,
- pristup iz vanjske mreže u lokalnu LAN mrežu je zabranjen,
- pristup iz DMZ u lokalnu mrežu je dozvoljen samo poslužitelju mail-relay koji dostavlja e-mail poslužitelju `mail` u lokalnoj mreži (protokol SMTP, port 25), sve ostale konekcije su zabranjene,
- iz vanjske mreže (Interneta) dozvoljen je pristup web poslužitelju `web` korištenjem protokola HTTP i HTTPS (portovi 80 i 443),
- iz vanjske mreže (Interneta) dozvoljen je pristup e-mail poslužitelju `mail-relay` korištenjem protokola SMTP (port 25),
- s poslužitelja `web` i `mail-relay` prema Internetu je dozvoljen pristup samo DNS poslužiteljima korištenjem protokola UDP i TCP (port 53),
- pristup vatrozidima FW i FW_int dozvoljen je samo s računala `int1` koje se nalazi u lokalnoj mreži i to korištenjem SSH (port 22),
- dodajte "anti-spoofing" pravila.

### Skripte za konfiguriranje vatrozida

U direktoriju zadatak3 nalaze se dvije shell skripte za konfiguriranje vatrozida (iptables): `FW.sh` i `FW_int.sh`.

Svoja pravila upisujete u proceduri `script_body`.

Skripte treba kopirati na odgovarajuće čvorove i tamo pokrenuti:

```
    $ sudo su
    # hcp FW.sh FW:
    # himage FW ./FW.sh start

    # hcp FW_int.sh FW_int:
    # himage FW_int ./FW_int.sh start
``` 

Ako se želi isključiti filtriranje prometa, skripta se može pozvati s argumentom "stop":

``` 
    # himage FW_int ./FW_int.sh stop
``` 

### Testiranje vatrozida

Provjera dostupnosti usluga u demilitariziranoj zoni računalima iz Interneta (čvor pc):
```
    himage pc nmap -n -Pn "-p20-25,53,80,443" 192.168.2.10
    himage pc nmap -n -Pn "-p20-25,53,80,443" 192.168.2.11
```

Provjera dostupnosti usluga u demilitariziranoj zoni računalima iz privatne mreže (čvor int1):
```
    himage int1 nmap -n -Pn "-p20-25,53,80,443" 192.168.2.10
    himage int1 nmap -n -Pn "-p20-25,53,80,443" 192.168.2.11
```

Provjera dostupnosti usluga u privatnoj mreži računalima iz Interneta (čvor pc):
```
    himage pc nmap -n -Pn "-p20-25,53,80,443" 192.168.1.10
```

Provjera dostupnosti usluga u privatnoj mreži računalima iz DMZ (čvorovi web i mail-relay):
```
    himage web nmap -n -Pn "-p20-25,53,80,443" 192.168.1.10
    himage mail-relay nmap -n -Pn "-p20-25,53,80,443" 192.168.1.10
```

## 4) Probijanje zaštite WEP za bežične mreže

U sklopu direktorija zadatak3 nalaze se dvije datoteke tipa pcap (packet
capture) koje sadrže pakete od napada na bežičnu mrežu zaštićenu s WEP načinom
šifriranja. S pomoću alata aircrack-ng pokušajte doći do lozinke za oba slučaja.

Proučite pcap datoteke u alatu Wireshark na svom operacijskom sustavu. U čemu se
te pcap datoteke razlikuju?

U postavkama Wiresharka za WLAN mreže (Izbornik Edit -> Preferences... ->
Protocols -> IEEE 802.11) stavite kvačicu na "Enable decryption" i dodajte unos
u "Decryption keys" koji sadrži WEP lozinku koju ste otkrili putem Wiresharka.
Proučite kakav se promet izmjenjuje s poslužiteljem 161.53.19.80 u datoteci
"SUI1_WEP.cap". Koje se datoteke dohvaća i putem kojeg protokola? (Poslužite se
opcijom "Follow TCP Stream")

## Rezultati laboratorijske vježbe

Kao rezultat laboratorijske vježbe **trebate predati** sljedeće podatke kroz
sustav Moodle nakon rješavanja vježbe:

- **izvještaj** o laboratorijskoj vježbi **u formular** na Moodlu (najviše
  **1000 riječi**) koji sadrži postupak rješavanja zadatka i odgovore na
  pitanja
- **ZIP arhivu** koja sadrži dvije datoteke: **popis naredbi** koje ste
  koristili za laboratorijsku vježbu u sklopu dodatne tekstualne datoteke
  `naredbe.txt` te vaše konačne verzije datoteka **FW.sh** i **FW_int.sh**.

## Alati korisni za izradu ove vježbe:

- `ping` - provjera mrežne povezivosti.
- `nmap` - skeniranje računala i servisa. Dohvaćate ga za svoj operacijski sustav
  (http://nmap.org/). Možete koristiti i Zenmap.
- `netstat` - pregled mrežnih servisa koji su trenutno pokrenuti na računalu.
- `service` - pokretanje i zaustavljanje servisa na operacijskom sustavu Debian.
- `iptables` - konfiguracija vatrozida na operacijskom sustavu Debian.
- `wireshark` - analiza mrežnog prometa. Dohvaćate ga za svoj operacijski sustav.
  (http://www.wireshark.org/)
- `aircrack-ng` - probijanje zaštite i pronalaženje lozinki bežičnih mreža.
