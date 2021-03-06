#!/bin/bash

#curl -i http://localhost:5000/photos/api/users

####

#Dokumentacija:
curl -i http://localhost:5000/photos/api/


#KORISNICI

#-dohvat svih korisnika:
curl -i http://localhost:5000/photos/api/users

#-dohvat jednog korisnika:

curl -i http://localhost:5000/photos/api/users/2
#- napravi novog korisnika:
curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Luka", "password":"rm"}' http://localhost:5000/photos/api/users

#-promijeni password:*
#curl -i -H "Content-Type: application/json" -X PUT -d '{"password":"strong"}' http://localhost:5000/photos/api/users/1

#SLIKE

#-dohvat svih slika:
curl -i http://localhost:5000/photos/api/pics

#-dohvat jedne slike:
curl -i http://localhost:5000/photos/api/pics/1

#-napravi novu sliku:
curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Football", "description":"slika"}' http://localhost:5000/photos/api/pics

#-promijeni naziv:
curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"Soccer"}' http://localhost:5000/photos/api/pics/1

#-dohvat slike jednog korisnika
curl -i http://localhost:5000/photos/api/users/2/pics

#autentifikacija
curl -u Ivan:python1 -i http://localhost:5000/photos/api/users/2/pics