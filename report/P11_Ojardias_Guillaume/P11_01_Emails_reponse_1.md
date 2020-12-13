Bonjour madame Jimena,

Je vous confirme que nous avons pris note de la menace en production relevée par vos équipes.

Le problème identifié à partir du commit [6ce2275](https://github.com/GuillaumeOj/P11-AddAFeature/commit/6ce2275ba3ff6730246e9b631c33cdce70ebc7e1) est le suivant :

- L'environnement de test en local utilise une base de données SQLite alors que les tests sur Travis utilisent comme en production une base de données PostgreSQL.

Nous allons donc procéder aux modifications suivantes :

- Unifier l'environnement de tests local avec celui de la production et de Travis en utilisant uniquement une base de données PostgreSQL.
- Apporter les correctifs nécessaires aux tests et au code pour corriger l'échec des tests.

Je reviens vers vous dans les heures qui suivent pour vous transmettre le commit de correction du code.

Cordialement,

Guillaume Ojardias.
