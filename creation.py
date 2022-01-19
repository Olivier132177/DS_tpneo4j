from neo4j import GraphDatabase

def creation(query):
    with driver.session() as session:
        session.run(query).data()

def loading_stations(): #LOADING DES STATIONS
    query = '''LOAD CSV WITH HEADERS FROM 'https://github.com/pauldechorgnat/cool-datasets/raw/master/ratp/stations.csv' AS row
    CREATE (: Station {nom_clean : row.nom_clean, 
    nom_gare : row.nom_gare, 
    latitude : toFloat(row.x),
    longitude : toFloat (row.y),
    trafic : toInteger(row.Trafic),
    ville : row.ville,
    ligne : row.ligne }) '''
    creation(query)

#LOADING DES LIAISONS

def loading_liaisons():
    query = '''LOAD CSV WITH HEADERS FROM 'https://github.com/pauldechorgnat/cool-datasets/raw/master/ratp/liaisons.csv' AS row
    MATCH (s1:Station) WHERE s1.nom_clean = row.start AND s1.ligne = row.ligne
    MATCH (s2:Station) WHERE s2.nom_clean = row.stop AND s2.ligne = row. ligne
    CREATE (s1)-[l:LIGNE]->(s2)
    SET l.distance = (((s1.latitude - s2.latitude)^2) + (s1.longitude - s2.longitude)^2)^0.5
    SET l.temps = l.distance * 60 / 40000'''
    creation(query)

#CREATION DES CORRESPONDANCES

def loading_correspondances():
    query = '''MATCH (s1:Station)
    MATCH (s2:Station) 
    WHERE s1.nom_clean = s2.nom_clean 
    AND s1.ligne <> s2.ligne
    CREATE (s1)-[c:CORR]->(s2)
    SET c.distance = 0
    SET c.temps = 4 '''
    creation(query)

#CREATION DES TRAJETS A PIED

def loading_trajets_a_pied():
    query = '''MATCH (s1:Station)
    MATCH (s2:Station) 
    WHERE s1.nom_clean <> s2.nom_clean
    AND (((s1.latitude - s2.latitude)^2) + (s1.longitude - s2.longitude)^2)^0.5 < 1000 
    CREATE (s1)-[a:APIED]->(s2)
    SET a.distance = (((s1.latitude - s2.latitude)^2) + (s1.longitude - s2.longitude)^2)^0.5
    SET a.temps = a.distance * 60 / 4000 '''
    creation(query)

def effacement_contenu():
    query='''MATCH (n) DETACH DELETE n'''
    creation(query)

driver = GraphDatabase.driver('bolt://0.0.0.0:7687',
                              auth=('neo4j', 'neo4j'))

effacement_contenu()
loading_stations()
loading_liaisons()
loading_correspondances()
loading_trajets_a_pied()


