

# Conception d'une base de données pour un site e-commerce : Olist (Brésil)

##### Team : Mickael Fayeulle, Antoine Dewynter, Arthur Telders



## Contexte du projet

Vous intégrez une société de e-commerce en tant que Developpeur IA et votre première mission consiste à les aider sur la refonte de leur base de données. La société a déjà récolté de la donnée et une première proposition a été réalisée. Cette proposition vous sera partagée ainsi que la donnée dans un second temps. La première étape de votre projet consiste à proposer votre vision sur la conception de la base de données.

Après votre proposition, votre équipe vous partagera le travail déjà réalisé et votre mission consitera à  mettre en commun votre travail et celle des équipes IT afin d'intégrer les données qui vous seront fournies à une base de données (SQL).



## Technologies utilisées

#### Phase 0 : Organisation du projet.

- Trello

#### Phase 1: Création du MPD.

- Draw.io

#### Phase 2: Partage du MPD des équipes, partage des données, Création de la DB.

- Python, Pandas, SQL, SQLite, Git, Github
- IDE : VS Code & Pycharm
- Visualisateur Git :  Gitkraken

#### Phase 3: Requêtage des donneés pour calculer les indicateurs.

- Jupyter Notebooks, Python, SQL



## Modèle physique de données (MPD)



MPD_Olist(1)



![](https://github.com/Hellfik/olist_ecommerce/blob/main/MPD_Olist(1).jpg)



Pour créer le MPD, nous avons repris les différentes tables et leurs colonnes fournies par les données originales qui se trouvent sur le site Kaggle.

Nous avons défini pour chaque table quelle était la clé primaire et quelles étaient les clés étrangères et les relations entre les différentes tables.

La table centrale est la table des commandes : 'olist_orders_dataset' autour de laquelle les autres tables s'articulent. 

Pour chaque colonne, nous avons choisi un type de données, dans le but d'optimiser la gestion de mémoire et de faciliter les calculs sur les heures et les dates.

Nous avons remarqué un problème dans la table 'olist_orders_items_dataset' qui représente chaque item (FK: product_id) et sa quantité (order_item_id) dans chaque commande (FK: order_id) .

En effet cette table n'a pas de clé primaire. Elle comporte 113k lignes. Pour pallier à ce problème, nous avons décidé de créer un id unique clé primaire en utilisant l'option AUTO_INCREMENT.

Nous avons intégré la table des traductions des catégories en anglais, qui n'était pas inclue dans le schéma fourni. 





## Création et intégration de la BDD étape par étape



Nous avons utilisé la bibliothèque SQLite3 pour créer et importer nos données, ce qui apporte l'avantage par rapport à MySQL de pouvoir créer la BDD directement sous forme d'un fichier '.db' , ce qui évite de devoir se connecter à un serveur pour y accéder.

Dans un premier fichier que nous nommons 'olist_tables.py' :

```python
import sqlite3
```



Nous avons initialisé une variable pour faire référence à notre fichier '.db', cette variable sert de paramètre à la méthode .connect() de l'object sqlite3, pour établir la connexion.

Nous avons ensuite initialisé un curseur pour effectuer des opérations  sur la base de données.

```python
DB_NAME = 'olist_db.db'

con = sqlite3.connect(DB_NAME)
cur = con.cursor()
cur.execute('pragma encoding=UTF8')
```



Nous avons ensuite créé les requêtes SQL de création de tables en utilisant le MPD, et nous les avons initialisées dans un dictionnaire 'TABLES'.



Exemple avec la table 'orders':

```python
TABLES['olist_orders_dataset'] = (
    '''CREATE TABLE olist_orders_dataset (
        order_id char(32) NOT NULL,
        customer_id char(32),
        order_status varchar(20),
        order_purchase_timestamp datetime,
        order_approved_at datetime,
        order_delivered_carrier_date datetime,
        order_estimated_customer_date datetime,
        order_estimated_delivery_date datetime,
        PRIMARY KEY (order_id),
        FOREIGN KEY (customer_id)
            REFERENCES customers_dataset(customer_id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
        )''' )
```



Grâce à une boucle for,  nous créons les tables de notre dictionnaire.

Pour terminer, nous effectuons une sauvegarde et fermons la connexion.

```python
# Create tables in dictionnary TABLES

for table_name in TABLES:
    table_description = TABLES[table_name]
    print("Creating table {}: ".format(table_name), end='')
    cur.execute(table_description)
    print("OK\n")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
```



Dans un second fichier que nous nommons 'olist_tables.py' :

Grâce à la bibliothèque pandas, nous allons importer les données des fichiers .csv de Kaggle que nous avons au préalable copiés dans un dossier /datasets.

```python
import sqlite3
import pandas as pd

DB_NAME = 'olist_db.db'

con = sqlite3.connect(DB_NAME)
cur = con.cursor()
cur.execute('pragma encoding=UTF8')
```



Exemple :

```python
"""
ORDERS DATAFRAME + WRITE INTO SQLITE TABLE

"""

orders_dataset = pd.read_csv('datasets/olist_orders_dataset.csv')
order_df = pd.DataFrame(orders_dataset)

order_df.to_sql(
    name="olist_orders_dataset",
    con=con,
    index=False,
    if_exists='replace',
    chunksize=500
)
```





### Évolution des variables : nos choix



'olist_order_reviews_dataset'

Il y a 99173 identifiants uniques de commentaires. Cependant la table comporte 100k lignes.

Nous avons remarqué que certains commentaires étaient assignés à plusieurs commandes avec la même date et heure et le même score.

Nous avons appliqué un drop_duplicate avec pandas sur la colonne 'review_id' de la table 'olist_reviews dataset'  pour éliminer les doublons.



'olist_geolocation_dataset'

Cette table comporte 1.00m de lignes de coordonnées GPS et leurs zipcodes, villes et états. Elle n'a pas de lien avec la table des clients, ni celle des vendeurs. 

Nous avons décidé de la nettoyer pour n'en conserver qu'une liste de zipcodes uniques en tant que clé primaire, avec leurs villes et états associés.

Le nombre de lignes après nettoyage devient 19015. Ceci nous permet d'établir la relation avec la table vendeurs et la table clients.



#### Remarques :

- 'product_category_name_translation'

  Cette table comporte 71 catégories traduites en anglais, mais il y a 74 catégories en portugais.

  Nous savons que parmi les 3 lignes manquantes, une d'entre elles s'appelle 'pc_gamer' . Une hypothèse serait que les catégories manquantes n'auraient pas été traduites parce qu'étant déjà en anglais.

- les colonnes 'product_name_lenght' et 'product_description_lenght' du fichier olist_products_dataset.csv comportent une faute d'orthographe au mot 'length'.
- il y a 99440 paiements pour 99441 commandes.
- 2% des commandes n'ont pas été envoyées.
- 3% des commandes n'ont jamais été livrées.







## Présentation du code SQL pour chaque indicateur



cf : Jupyter Notebook 'indicator_queries.ipynb'



