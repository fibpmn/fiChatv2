### Svuečilište Jurja Dobrile u Puli
### Fakultet informatike u Puli
#### Web aplikacija Fibot/Završni rad
#
##### Autori: Bernobić Nikki, Starčić Toni
##### Mentor: doc. dr. sc. Darko Etinger
##### Komentor: doc. dr. sc Nikola Tanković
#
#### Koraci za pokretanje aplikacije
#
###### 1. Preuzmite projekt i raspakirajte ga.
#
###### 2. Posebno raspakirajte "camunda-bpm-tomcat-7.13.0" koji sadrži dijagrame procesa i definirane profile.
#
###### 3. U raspakiranom direktoriju pronaći ćete "start-camunda.bat" i "start-camunda.sh". Ovisno o OS-u, pokrenite skriptu.
##### Napomena: Ukoliko nemate Javu na računalu, preuzmite i instalirajte ju. P.S Nemojte zaboraviti na PATH environment varijablu :)
##### Poveznica: https://java.com/en/download/
#
###### 4. Kada se podigne server, trebali bi vidjeti ovu sliku: 
![Alt text](https://i.imgur.com/Aoneq4Il.png)
#
###### 5. Kliknite na Camunda Cockpit, unesite podatke. Pomoću Camunda Cockpita možete pratiti izvršavanje procesne instance. 
![Alt text](https://i.imgur.com/iGYiyEul.png")
#
###### 6. Instalirajte dependenciese
###### 6.1 Za javascript
```
yarn install
```
###### 6.2 Za python
```
cd flask
pip3 install -r requirements.text
```
#
###### 7. Pokrenite server za front end
```
yarn serve
```
#
###### 8. Pokrenite server za back end
```
yarn start-flask
```
#
###### Prikaz korištenja aplikacije:
[![Watch the video](https://i.imgur.com/5mOA1xZ.png)](https://www.youtube.com/watch?v=SlvPC0xSRMA)
###### Happy version korištenja aplikacije:
[![Watch the video](https://i.imgur.com/CqYJuCP.png)](https://www.youtube.com/watch?v=bLNqvGln4sM)
#
###### Korisnički podaci za Camundu
###### username: DarkoEtinger
###### username: NikolaTankovic
###### username: SinisaMilicic
###### passwords: 12345
###### admin username: demo
###### admin password: demo
#
###### Korisnički podaci za aplikaciju
###### email: darko.etinger@unipu.hr
###### email: nikola.tankovic@unipu.hr
###### email: sinisa.milicic@unipu.hr
###### email: nikki.bernobic@unipu.hr
###### email: toni.starcic@unipu.hr
###### passwords: test
#
##### Bernobić Nikki
##### Sažetak
######
Chatbot sustavi postoje tek oko pedesetak godina no sve su popularniji zbog njihove široke primjene – danas ih se može vidjeti gotovo u svakom području. U svakodnevnom životu viđamo ih kao Alexa, Google, Siri ili kao jednostavnije chatbotove koji se pojavljuju na web stranicama te služe za odgovaranje na često postavljana pitanja ili za pomoć pri kupnji. Tvrtke koriste ovakve sustave kako bi smanjili izdatke budući da jedan dobro izrađen chatbot nema radno vrijeme, efikasan je i drastično smanjuje upite korisnika. Pitanje koje si postavljamo jest zašto ograničiti korisnost chatbotova samo na odgovaranje upita korisnika?
######
#
##### Starčić Toni
##### Sažetak
######
Sustavi raznih organizacija, kao što su poduzeća ili javne službe, sastoje se od složenih procesa koje nije moguće unaprijediti eksperimentiranjem u realnom vremenu, pa se iz toga razloga razvijaju modeli tih poslovnih procesa kako bi se izvela nova rješenja čiji je ultimativni cilj – automatizacija poslovnih procesa. Disciplina ili sistematska metoda promatranja poslovnih procesa jest Upravljanje poslovnim procesima (eng. Business Process Management) koja se koristi za otkrivanje, modeliranje, analizu, mjerenje, poboljšanje, optimizaciju i automatizaciju poslovnih procesa. „Prema genetičkoj je definiciji poslovni proces … povezani skup aktivnosti i odluka, koji se izvodi na vanjski poticaj radi ostvarenja nekog mjerljivog cilja organizacije, traje određeno vrijeme i troši određene resurse pretvarajući ih u specifične poizvode ili usluge važne za kupca ili korisnika.“  
Kao jedan od praktičnih primjera automatizacije generalno, pa tako i procesne automatizacije, su konverzacijski agenti (eng. Chatbots). Konverzacijski agent je softverska aplikacija koja nudi mogućnost konverzacije, a posebno je koristan u situacijama gdje je interakcija naglašena, odnosno dijalog.
Naime, dijalog je najprirodniji način komunikacije kod ljudi, a od računalnih početaka, znanstvenici su nastojali razviti što je moguće prirodniju komunikaciju čovjeka sa strojem. Prvi takav konverzacijski agent, odnosno računalni program napravljen je prije pola stoljeća na MIT-evom laboratoriju za umjetnu inteligenciju naziva „ELIZA“. Danas, pola stoljeća kasnije, konverzacijski agenti su primjenjivi gotovo u svim granama gospodarstva i time imaju visoku komercijalnu vrijednost. 
„Fibot“ je web aplikacije koja je razvijena u svrhu završnog rada kao dokaz o konceptu spajanja modela poslovnog procesa i konverzacijskog agenta. Zašto su modeli i konverzacijski agenti međusobno komplemetarni? Model omogućuje analizu i optimizaciju, a sam chatbot se može promatrati kao sučelje ili kao pogon tog istog modela.  
U radu će biti prikazano programsko rješenje i implementacija, s time da će se spomenuti i Camunda platforma koja omogućuje samu implementaciju. Osim Camunde bit će spomenuta arhitektura i struktura aplikacije, a poseban je naglasak na objašnjenju načina rada programskog sučelja.
######
