# Mon Projet d'API RATP

C'est une application FastAPI simple qui fait du web scraping sur le site `www.ma-ligne.co` pour obtenir des informations sur le trafic.

## Exécution de l'application

Pour exécuter l'application, vous pouvez utiliser Docker Compose avec la commande suivante :

```bash
docker-compose up
```

Ensuite, vous pouvez accéder à l’application [ici](http://localhost:6001) 

## Utilisation de l’API
Le route `/traffic/{transport_type}/{transport_id}` possède deux variables :**transport_type** est le type de transport (bus, metro, etc.) et **transport_id** est l’identification du transport. Cette route retourne des informations sur le trafic pour le type de transport et l’identification donnés.

### TODO
- Ajouter les temps de transports,
- Ajouter la quantité de passages selon l'heure actuelle.
