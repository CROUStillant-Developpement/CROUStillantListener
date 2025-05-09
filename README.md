<div align="center">
<img src="https://croustillant.menu/logo.png" alt="CROUStillant Logo"/>
  
# CROUStillant Listener
CROUStillant est un projet qui a pour but de fournir les menus des restaurants universitaires en France et en Outre-Mer. 

</div>
  
# 📖 • Sommaire

- [🚀 • Présentation](#--présentation)
- [📦 • Installation](#--installation)
- [📃 • Crédits](#--crédits)
- [📝 • License](#--license)

# 🚀 • Présentation

Ce dépôt contient le "listener", un script qui détecte l'ajout des nouveaux restaurants dans la base de données. 

# 📦 • Installation

Pour installer CROUStillant Listener, vous aurez besoin de [Docker](https://www.docker.com/) et de [Docker Compose](https://docs.docker.com/compose/).

Pour cloner le dépôt, exécutez la commande suivante :
```bash
git clone https://github.com/CROUStillant-Developpement/CROUStillantListener
```

Il vous faudra ensuite créer un fichier `.env` à la racine du projet, contenant les variables d'environnement suivantes :
```env
# Postgres
POSTGRES_DATABASE=CROUStillant
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Discord
DISCORD_WEBHOOK=
```

Pour lancer CROUStillant Listener, exécutez la commande suivante :
```bash
docker-compose up
```

# 📝 • License

CROUStillant sous licence [Apache 2.0](LICENSE).

```
Copyright 2024 - 2025 CROUStillant Développement

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
