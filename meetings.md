# Meetings notes

## Meeting 1.
* **DATE: 12.02.2021**
* **ASSISTANTS: Mika Oja**

### Minutes
Restful API description (Initial API idea)

### Action points
Overview otsikon alle:
- lisää kuvaus että haetaan dataa external APIsta

API uses otsikon alle:
-voisi lisätä myös että mitä osia api:sta clientit käyttää


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 2.
* **DATE: 03.03.2021**
* **ASSISTANTS: Mika Oja**

### Minutes
Database design and implementation

### Action points
- poista relaatiot taulukoista

- portfolio-user suhdetta ei määritetä kahteen suuntaan
    -tulee relationshipin kautta
    -useraccountista portfolio_id pois

- check constraint positiivisille luvuille

- ondelete/onupdate = CASCADE/SET NULL/PROTECT määritykset (protect ei anna poistaa niin kauan kuin viitataan, esim cryptocurrencyä ei voi poistaa)

- siirrä "rimpsu" myös appiin (pitää olla testeissä ja appissa)

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 3.
* **DATE: 24.03.2021**
* **ASSISTANTS: Mika Oja**

### Minutes
Restful API design

### Action points
- nuoli portfoliocurrencyn ja cryptocurrencyn välille
- enemmän linkkejä resurssien välillä
- poista edit Apiaryssä (on standardi)
- portfoliocurrency collectionissa voisi lisätä myös nimen items-kohdissa / Profiles-kohdassa (Apiaryssä)
- lue Extra chapter: Managing relations
- poista password Account listauksista (jotain yritystä tietoturvan suhteen)

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 4.
* **DATE: 15.4.2021**
* **ASSISTANTS: Mika Oja**

### Minutes
Restful API implementation

### Action points
- lisää linkkejä kurssimateriaaleihin + esimerkkiprojektiin mistä otettu mallia

- tsekkaa että currencyamount ei voi olla negatiivinen

- tsekkaa portfolion luominen accountille

- paranna dokumentaatiota

- katso cov-reportista testaamattomat rivit ja lisää testejä


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Midterm meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Final meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

