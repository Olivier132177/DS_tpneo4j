from neo4j import GraphDatabase
from pprint import pprint

driver = GraphDatabase.driver('bolt://0.0.0.0:7687',
                              auth=('neo4j', 'neo4j'))

def exec_requete(query):
    with driver.session() as session:
        result = session.run(query).data()
    pprint(result)

def creation(query):
    with driver.session() as session:
        session.run(query).data()

def creation_point_de_depart(lati_dep, long_dep):
    query = "CREATE (n:Station:Temp {{ nom_clean : 'DEPART', nom_gare : 'DEPART',\
        latitude : {} ,longitude : {},trafic : 0, ville : '',ligne : ''}})".format(lati_dep, long_dep)
    creation(query)

def creation_point_d_arrivee(lati_arr,long_arr):
    query = "CREATE (n:Station:Temp {{ nom_clean : 'ARRIVEE', nom_gare : 'ARRIVEE',\
        latitude : {} ,longitude : {},trafic : 0, ville : '',ligne : ''}})".format(lati_arr, long_arr)
    creation(query)

def creation_liaisons_depart(): # CREATION DES LIAISONS A PIED VERS LES STATIONS
    query = '''MATCH (t:Temp) MATCH (s:Station) 
    WHERE t.nom_clean <> s.nom_clean
    AND t.nom_clean = 'DEPART'
    WITH id(s) as identif, s,(((t.latitude - s.latitude)^2) + (t.longitude - s.longitude)^2)^0.5 as distance ORDER BY distance LIMIT 3
    MATCH (t:Temp)
    WHERE t.nom_clean = 'DEPART'
    CREATE (t)-[a:APIED]->(s)
    SET a.distance = distance
    SET a.temps = distance * 60 / 4000 
    RETURN identif, distance, s.nom_clean, s.ligne'''    
    exec_requete(query)

def creation_liaisons_arrivee(): # CREATION DES LIAISONS A PIED VERS LES STATIONS
    query = '''MATCH (t:Temp) MATCH (s:Station) 
    WHERE t.nom_clean <> s.nom_clean
    AND t.nom_clean = 'ARRIVEE'
    WITH id(s) as identif, s,(((t.latitude - s.latitude)^2) + (t.longitude - s.longitude)^2)^0.5 as distance ORDER BY distance LIMIT 3
    MATCH (t:Temp)
    WHERE t.nom_clean = 'ARRIVEE'
    CREATE (t)<-[a:APIED]-(s)
    SET a.distance = distance
    SET a.temps = distance * 60 / 4000 
    RETURN identif, distance, s.nom_clean, s.ligne'''    
    exec_requete(query)

def calcul_temps_trajet(): # CALCUL DU TEMPS DE TRAJET ENTRE LES 2 POINTS
    que='''
    MATCH (start:Temp {nom_clean: 'DEPART'})
    MATCH (end:Temp {nom_clean: 'ARRIVEE'})
    CALL gds.alpha.shortestPath.stream({
    nodeQuery: 'MATCH (n) RETURN id(n) as id',
    relationshipQuery: 'MATCH (n1)-[r]-(n2) RETURN id(r) as id, id(n1) as source, id(n2) as target, r.temps as weight',
    startNode: start,
    endNode: end,
    relationshipWeightProperty: 'weight'
    })
    YIELD nodeId, cost
    WITH nodeId, cost
    MATCH (m)
    WHERE id(m) = nodeId
    RETURN m.ligne, m.nom_clean, cost'''
    exec_requete(que) 

def suppression_points(): # SUPPRESSION DES NOEUDS TEMPORAIRES
    exec_requete('''MATCH (n:Temp) DETACH DELETE n
    ''')

lati_dep=641552 # LATITUDE DEPART
long_dep=6862000 # LONGITUDE DEPART
lati_arr=652510 # LATITUDE ARRIVEE
long_arr=6859715 # LONGITUDE ARRIVEE

creation_point_de_depart(lati_dep,long_dep)
creation_point_d_arrivee(lati_arr,long_arr)
creation_liaisons_depart()
creation_liaisons_arrivee()
calcul_temps_trajet()
suppression_points()


