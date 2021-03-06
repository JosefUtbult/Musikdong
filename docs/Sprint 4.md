# Sprint 4 - Slutrapport

## Introduction

Det här är en webbshop utvecklad för en laboration i kurset _D0020E_. _Musikdong_, som är webbshopens namn, säljer gitarrpedaler, fullt legala tjänster samt annat smått och gott. Nu är sidan färdig och sitter sidan uppe på IP-adressen http://130.240.200.51:5000. Servern är aktiv om man ber Josef att sätta på den, annars ligger den passiv.

## Executive summary - Sprint 1

### Josef

Jag har jobbat med att sätta upp servern inför sprint 1. Vi använde den virtuella maskinen tillhandahållen av LUDD, där vi satt upp mySql som databas, en flask-applikation för att kommunicera med backenden samt Nginx för att komma åt sidan via vår statiska IP.

Jag har även experimenterat med att interagera med mySql, främst på min egen maskin för enkelhetens skull, men sett till så att allt är kompatibelt för att emigrera till den virtuella maskinen.

### Leo

Jag har tillsammans med Josef tagit fram user stories samt gjort en enkel hemsida med html och css. 

## Executive summary - Sprint 2

### Josef

Jag har byggt om databasen för att hantera produkter, kategorier och användare mm. Jag har även lagt till strukturen för orderhantering i databasen, i form av ett orders-table och ett orderItem-table. En grundläggande manager-sida har också lagts till.

## Executive summary - Sprint 3

Jag har byggt klart manager-sidan med möjlighet att lägga till produkter och kategorier, samt redigera användare, produkter och kategorier. Jag har fixat orderhanteringen och implementerat att priset låses efter att ordern läggs. Jag har även implementerat reviws. 

## Executive summary - Sprint 4

Jag har lagt till en sökbar i headern som söker på produktnamn.

# Userstories

## Admin

1. Har alla rättigheter som manager.
2. Kan ändra rättigheter för alla användare på sidan.
3. Kan lägga till och radera
	+ Kategorier
	+ Tagtyper

## Manager

1. Har alla rättigheter som en inloggad användare.
2. Kan öppna en manager meny.
3. Har tillgång till att redigera alla
  + Användare
  + Produkter
  + Kategorier 
  + Tagtyper
  + Reviews
  + Carts
  + Orders

4. Kan få en lista med alla ordrar i manager-menyn, där man ser betalade ordrar samt hanterade ordrar separat.
5. Kan lägga till och radera
  + Användare
  + Produkter
  + Taggar
  
## Inloggad användare

1. Har alla rättigheter som en icke inloggad användare.
2. Kan orientera sig mellan kategorier till produkter.
3. Kan lägga produkter i sin kundvagn.
4. Kan lägga en review på en produkt.
5. Kan öppna sin kundvagn och se vad som ligger i.
6. Kan lägga en order som senare hanteras av managers.
7. Kan logga ut från sin användare.

## Icke inloggad användare

1. Kan orientera sig mellan kategorier till produkter.
2. Kan använda sökbaren för att söka på ett produktnamn.
3. Kan logga in, eller skapa en användare.

# Nuvarande Backlog

![](https://snipboard.io/oKrlJq.jpg)

# ER-diagram

![](https://snipboard.io/otvX8T.jpg)

# Kodbas

Koden finns tillgänglig publikt på Github under min användare (JosefUtbult). Där ligger även backloggen i form av issues.
``` https://github.com/JosefUtbult/Musikdong/```

# Tester

## Icke inloggad användare

### Hitta en produkt

1. Öppna startsida.
2. Navigera till en kategori.
3. Navigera till en produkt.
4. Öppna sida för produkt.

### Sök efter produkt
1. Navigera till sökbaren.
2. Skriv in namn eller del av namn på en produkt.
3. Tryck på _Sök_.
4. Välj produkt bland resultaten.

### Skapa användare

1. Tryck på _Sign Up_.
2. Välj ett användarnamn.
	+ Det ska inte gå att välja ett användarnamn som redan är registrerad.
3. Välj lösenord.
4. Skapa användare.

### Logga in

1. Tryck på _Login_.
2. Skriv in användarnamn och lösenord.
3. Logga in.

## Inloggad användare

### Lägg vara i kundvagn

1. Navigera till en vara.
2. Lägg i kundvagn.

### Visa kundvagn

1. Tryck på kundvagn i headern.

### Lägg order

1. Öppna kundvagnen.
2. Lägg order.

### Lägg review

1. Navigera till en produkt.
2. Använd slidern för att ställa in ett betyg mellan ett till fem.
3. Skriv en review.
4. Tryck på _review_.

## Manager

### Visa produkt/användare/ordrar

1. Tryck på _Manager_ i headern.
2. Navigera till produkt/användare/ordrar
3. Öppna sida för produkt/användare/ordrar

### Redigera produkt/användare/ordrar

1. Navigera till produkt/användare/ordrar
2. Redigera produkt/kategori/ordrar
3. Tryck på _Update_

### Lägga till produkt

1. Öppna _Manager_.
2. Tryck på _Add_
3. Fyll i produkt
4. Tryck på _Add_.

### Radera produkt/användare/ordrar

1. Navigera till produkt/användare/ordrar
2. Redigera produkt/användare/ordrar
3. Tryck på _Delete_

## Admin

### Updatera kategori/rättigheter
1. Utförs på samma sätt som produkt/användare/ordrar

### Radera kategor
1. Utförs på samma sätt som produkt/användare/ordrar

## Limitations

### Säkerhet

Sidan inkluderar en sökbar som skickar ett sök-request till servern. Detta request hanteras av Pymysqls inbyggda formatering av requests, men utöver det görs ingen säkerhetscheck på indatan. Detta kan i teorin släppa igenom vissa SQL-injektioner.

### Review

En användare kan endast lägga en review per produkt. Detta då databasen använder en tuple av _userId_ och _productId_ som primär nyckel samt att GUIn bygger på att man kan lägga en review och senare kan redigera denna. Huruvida detta är att föredra går att diskutera, men jag har valt att implementera den såhär.

### Taggar

Taggar samt taggtyper var en ide för att möjliggöra en sökfunktion. Detta finns färdigt i databasen, men implementationen blev nedprioriterat. Tanken från början var att taggar skulle inkluderas i sökresultaten då en användare använder sökbaren, men denna implementationen nedprioriterades tills den inte lägre var väsentlig för projektet.

### Produktbilder

URL för bilder på produkter är även tillagt i databasen, men tillägning av bilder, lagring samt visning av bilder på produktsidor blev inte implementerat i programmet.