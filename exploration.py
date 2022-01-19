from neo4j import GraphDatabase
from pprint import pprint


def exec_requete(query):
    with driver.session() as session:
        result = session.run(query).data()
    pprint(result)


def question1 (): 
  #Quel est le nombre de correspondances par station ?
  que='''MATCH (n)-[r:CORR]->(m)
  RETURN n.ligne as ligne, count(*) as nb_correspondances'''
  exec_requete(que)


def question2 ():
  #Quel est le nombre de stations à moins de deux kilomètres de la station LADEFENSE 
  # (on pourra prendre la distance brute sans considération de relation) ?

  que='''MATCH (n:Station {nom_clean:"LADEFENSE"})
  MATCH (m:Station)
  WHERE (((n.latitude - m.latitude)^2 + (n.longitude - m.longitude)^2) ^(0.5) < 2000)
  AND m.nom_clean <> n.nom_clean
  RETURN count(m.nom_clean) as stations_a_moins_de_2_km'''
  exec_requete(que)

def question3 ():
  #Combien de temps faut-il pour aller en metro de LADEFENSE à CHATEAUDEVINCENNES ?

  que='''
  MATCH (start:Station {nom_clean: 'LADEFENSE'})
  MATCH (end:Station {nom_clean: 'CHATEAUDEVINCENNES'})
  CALL gds.alpha.shortestPath.stream({
    nodeQuery: 'MATCH (n) RETURN id(n) as id',
    relationshipQuery: 'MATCH (n1)-[r]-(n2) RETURN id(r) as id, id(n1) as source, id(n2) as target, r.temps as weight',
    startNode: start,
    endNode: end,
    relationshipWeightProperty: 'weight'
  })
  YIELD nodeId, cost
  WITH nodeId, cost
  RETURN max(cost) as temps_en_min'''
  exec_requete(que)


def question4 ():
  #Combien de temps faut-il pour aller à pied de LADEFENSE à CHATEAUDEVINCENNES (on pourra considérer que t
  # out le chemin se fait à pied, sans considération de relation) ?

  que='''MATCH (s1:Station)
  MATCH (s2:Station)
  WHERE s1.nom_clean = 'CHATEAUDEVINCENNES' 
  and s2.nom_clean = 'LADEFENSE' 
  RETURN ((s1.latitude - s2.latitude)^2 + (s1.longitude - s2.longitude)^2) ^(0.5) *60 / 4000 as temps_en_min'''
  exec_requete(que)


def question5():
  #Est-il plus rapide de faire un changement à SAINTLAZARE pour aller de MONTPARNASSEBIENVENUE à GABRIELPERI ?

  que='''
  MATCH (start:Station {nom_clean: 'MONTPARNASSEBIENVENUE', ligne:'13'})
  MATCH (end:Station {nom_clean: 'GABRIELPERI'})
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
  print(' Réponse : Le plus rapide est de ne pas faire de changement')

def question6():
  #Combien de stations se trouvent dans un rayon de 10 stations par train autour de SAINTLAZARE ?

  que='''MATCH (s1:Station {nom_clean : 'STLAZARE'})-[:LIGNE|:CORR*..10]->(s2:Station)
  WHERE s2.nom_clean <> s1.nom_clean
  RETURN count(DISTINCT (s2.nom_clean)) as nombre_stations_rayon_10_stations'''
  exec_requete(que) 

def question7():
  #Combien de stations se trouvent dans un rayon de 20 minutes par train autour de SAINTLAZARE ?

  que='''
  MATCH (start:Station {nom_clean: 'STLAZARE'})
  MATCH (end:Station)
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
  AND cost < 20
  RETURN m.nom_clean, min(cost) as temps_de_trajet ORDER BY temps_de_trajet
  '''
  exec_requete(que) 


driver = GraphDatabase.driver('bolt://0.0.0.0:7687',
                              auth=('neo4j', 'neo4j'))


question1()   
#Quel est le nombre de correspondances par station ?

question2()   
#Quel est le nombre de stations à moins de deux kilomètres de la station LADEFENSE 
#(on pourra prendre la distance brute sans considération de relation) ?

question3()   
#Combien de temps faut-il pour aller en metro de LADEFENSE à CHATEAUDEVINCENNES ?

question4()   
#Combien de temps faut-il pour aller à pied de LADEFENSE à CHATEAUDEVINCENNES (on pourra 
#considérer que tout le chemin se fait à pied, sans considération de relation) ?

question5()   
#Est-il plus rapide de faire un changement à SAINTLAZARE pour aller de MONTPARNASSEBIENVENUE à GABRIELPERI ?

question6()   
#Combien de stations se trouvent dans un rayon de 10 stations par train autour de SAINTLAZARE ?

question7()   
#Combien de stations se trouvent dans un rayon de 20 minutes par train autour de SAINTLAZARE ?