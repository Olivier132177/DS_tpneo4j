TP Neo4J

A Les données

    2 fichiers :

    stations.csv : contient des informations sur les stations
    liaisons.csv : contient des informations sur les liaison entre stations

 A1 stations.csv

    nom_clean : nom de la station en majuscule
    nom_gare : nom de la station
    x : latitude en m
    y : longitude en m
    Trafic : le trafic estimé sur une année
    Ville : ville dans laquelle se trouve la station
    ligne : numéro de la ligne qui passe par la station

Dans ce fichier, une gare revient autant de fois qu'il y a de lignes qui passe par elle :

 A2 liaisons.csv

    start : station de début de la liaison
    stop : station de fin de la liaison
    ligne : ligne de la liaison

Dans ce fichier, les liaisons se trouvent dans les deux sens (faire attention à la ligne 10 et à la ligne 7bis) :


B Le graphe

	On veut construire un graphe qui permet de représenter les stations, les liaisons par train, les liaisons à pied et les correspondances.
        On choisira donc de créer un nœud pour chaque ligne qui passe par chaque station. Avec l'exemple donné précédemment, la station Arts et Métiers
        sera représentée par deux nœuds : un pour la ligne 3 et un pour la ligne 11..

	On pourra créer une relation entre ces deux nœuds pour représenter la correspondance par une relation. Cette relation pourra être représentée dans les deux sens.
	Entre deux stations qui sont sur la même ligne, on pourra représenter la liaison par une relation. Cette relation doit être représentée dans les deux sens.

	Enfin, entre deux stations qui sont espacées de moins d'un kilomètre (en ligne droite : on pourra utiliser la fonction SQRT), 
	on pourra créer une relation correspondant aux personnes pouvant se déplacer à pied entre deux stations.

	On estimera qu'une correspondance prend 4 minutes. On estimera aussi qu'un métro se déplace à une vitesse de 40km/h et une personne à 4km/h.
	On utilisera les coordonnées x, y des stations pour calculer la distance entre deux stations.
	
C Les consignes
 C1 Création du graphe

	Le premier objectif à remplir est la remise d'un fichier contenant les instructions pour construire un tel graphe.
	Exploration

	Le deuxième objectif et la remise d'un fichier contenant les instructions pour répondre aux questions suivantes :

	    Quel est le nombre de correspondances par station ?
	    Quel est le nombre de stations à moins de deux kilomètres de la station LADEFENSE (on pourra prendre la distance brute sans considération de relation) ?
	    Combien de temps faut-il pour aller en metro de LADEFENSE à CHATEAUDEVINCENNES ?
	    Combien de temps faut-il pour aller à pied de LADEFENSE à CHATEAUDEVINCENNES (on pourra considérer que tout le chemin se fait à pied, sans considération de relation) ?
	    Est-il plus rapide de faire un changement à SAINTLAZARE pour aller de MONTPARNASSEBIENVENUE à GABRIELPERI ?
	    Combien de stations se trouvent dans un rayon de 10 stations par train autour de SAINTLAZARE ?
	    Combien de stations se trouvent dans un rayon de 20 minutes par train autour de SAINTLAZARE ?

	Application

	Le dernier objectif de ce projet est de créer un moteur de calcul d'itinéraire sous la forme d'un script ou d'une fonction Python qui prend en entrée deux points représentés
	par leurs coordonnées (x, y) et qui renvoie l'itinéraire le plus efficace à suivre pour aller du premier au deuxième en affichant les noms des stations et des lignes à prendre 
	ainsi que le temps total. Bien évidemment cette fonction devra utiliser CYPHER et la librairie neo4j de Python : l'utilisation de Python est ici surtout destinée à intégrer ce 
	script dans une API et traiter facilement la modification des arguments. Pour créer cette fonction, il faudra utiliser l'algorithme de Djikstra vu précédemment. On pourra créer 
	deux nœuds éphémères pour représenter les points de départ et d'arrivée et des relations éphémères qui pourront être supprimées à chaque nouvelle itération.Le rendu attendu est
	un script Python qui couvre ces demandes.
	
d Évaluation

	Les attendus pour ce projet sont donc la remise de ces trois fichiers. Ces fichiers devront être en mesure de fonctionner avec le container Docker datascientest/neo4j. 
	Pour les deux premiers fichiers, les commandes proposées doivent être en mesure de fonctionner si elles sont tapées dans la console. Pour le dernier fichier, il faudra que seule 
	la partie gestion des arguments soit codée avec Python : tout le reste doit être fait avec CYPHER.

	Bon courage !
