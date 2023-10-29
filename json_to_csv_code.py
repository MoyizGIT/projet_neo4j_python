import json
import argparse
import os.path as path

# SCRIPT PARAMETERS
parser = argparse.ArgumentParser(description='Conversion JSON to CSV')

parser.add_argument('-l', '--lecture', required=True, help='Chemin/dossier des fichiers JSON.')
parser.add_argument('-e', '--ecriture', required=True, help='Chemin/dossier écriture noeud/relation.')
param = parser.parse_args()

print(param.lecture)
print(param.ecriture)


# EMPLACEMENT D'ECRITURE DES FICHIERS DE NOEUDS ET RELATIONS
#RESTAURANT

chemin = path.join(param.lecture, "yelp_user.json")
chemin2 = path.join(param.lecture, "yelp_review.json")
chemin3 = path.join(param.lecture, "yelp_restaurants.json")
chemin4 = path.join(param.ecriture, "restaurant.csv")
chemin5 = path.join(param.ecriture, "city.csv")
chemin6 = path.join(param.ecriture, "categorie.csv")
chemin7 = path.join(param.ecriture, "ambiance.csv")
chemin8 = path.join(param.ecriture, "price.csv")
chemin9 = path.join(param.ecriture, "sesitue.csv")
chemin10 = path.join(param.ecriture, "estinclus.csv")
chemin11 = path.join(param.ecriture, "contient.csv")
chemin12 = path.join(param.ecriture, "propose.csv")
chemin13 = path.join(param.ecriture, "user.csv")
chemin14 = path.join(param.ecriture, "data.csv")
chemin15 = path.join(param.ecriture, "amitie.csv")
chemin16 = path.join(param.ecriture, "possede.csv")
chemin17 = path.join(param.ecriture, "review.csv")
chemin18 = path.join(param.ecriture, "poste.csv")
chemin19 = path.join(param.ecriture, "commente.csv")

fichiernoeudrestaurant = open(chemin4, "w")
fichiernoeudcity = open(chemin5, "w")
fichiernoeudcategorie = open(chemin6, "w")
fichiernoeudambiance = open(chemin7, "w")
fichiernoeudprice = open(chemin8, "w")
fichierrelationsesitue = open(chemin9, "w")
fichierrelationestinclus = open(chemin10, "w")
fichierrelationcontient = open(chemin11, "w")
fichierrelationpropose = open(chemin12, "w")
#USER
fichiernoeuduser = open(chemin13, "w")
fichiernoeuddata = open(chemin14, "w")
fichiernrelationfriends = open(chemin15, "w")
fichiernrelationdata = open(chemin16, "w")
#REVIEW
fichiernoeudreview = open(chemin17, "w")
fichierrelationposte = open(chemin18, "w")
fichierrelationcommente = open(chemin19, "w")


# DECLARATION DES NOEUDS
noeuduser = "user:ID,name,:LABEL" + "\n"
noeudata = "data:ID,reviewcount:int,fan:int,:LABEL" + "\n"
noeudreview="review:ID,star:float,cool:int,useful:int,:LABEL"+ "\n"
noeudrestaurant="restaurant:ID,namer,:LABEL"+ "\n"
noeudcity="city:ID,:LABEL"+ "\n"
noeudambiance="ambiance:ID,:LABEL"+ "\n"
noeudprice="price:ID,:LABEL"+ "\n"
noeudcategorie="categorie:ID,:LABEL"+ "\n"

# DECLARATION DES RELATIONS:
relationfriends = ":START_ID,:END_ID,:TYPE" + "\n"
relationdata = ":START_ID,:END_ID,:TYPE" + "\n"
relationposte = ":START_ID,:END_ID,:TYPE" + "\n"
relationcommente = ":START_ID,:END_ID,:TYPE" + "\n"
relationsesitue = ":START_ID,:END_ID,:TYPE" + "\n"
relationestinclus = ":START_ID,:END_ID,:TYPE" + "\n"
relationcontient = ":START_ID,:END_ID,:TYPE" + "\n"
relationpropose= ":START_ID,:END_ID,:TYPE" + "\n"

# INDICES ET LISTES
idval0 = 0  # Indice de data
listecity = []  # Liste pour stocker la ville et son indice
listecategorie = [] # Liste pour stocker la catégorie et son indice
listeambiance = [] # Liste pour stocker l'ambiance et son indice
listeprice = [] # Liste pour stocker le prix et son indice

#CHARGEMENT DU FICHIER USER.JSON
with open(chemin) as f:
    for line in f:
        j_content = json.loads(line)
        for i in range (0,len(j_content)): #Parcourir le fichier JSON
            idval0+=1 #Compteur pour incrémenter les indices des ID des noeuds
            friends = j_content[i]['friends'] #Récupérer la liste des amis de User

            #NOEUD USER ET DATA
            noeuduser=noeuduser+j_content[i]['user_id']+","+j_content[i]['name']+",user"+"\n" #Chaine de caractère pour le noeud USER
            noeudata =noeudata+"data"+str(idval0)+","+str(j_content[i]['review_count'])+","+str(j_content[i]['fans'])+",data"+"\n" #Chaine de caractère pour le noeud DATA

            #RELATION POSSEDE ET AMITIE
            relationdata=relationdata+j_content[i]['user_id']+","+"data"+str(idval0)+","+"possede"+"\n" #Chaine de caractère pour la relation POSSEDE entre USER et DATA
            if friends is not None: #Si le user n'a pas d'amis alors on ne créee pas la relation pour cet utilisateur
                for j in range (1,len(friends)): #Parcourir la liste des amis de l'utilisateur
                    relationfriends =relationfriends+j_content[i]['user_id']+","+friends[j]+","+"amitie"+"\n" #Chaine de caractère pour la relation AMITIE entre USER et USER


#CHARGEMENT DU FICHIER REVIEW.JSON
with open(chemin2) as f:
    for line in f:
        j_content = json.loads(line)
        for i in range(0, len(j_content)):

            # NOEUD REVIEW:
            noeudreview = noeudreview + j_content[i]['review_id']+ "," + str(j_content[i]['stars'])+ ","+str(j_content[i]['cool'])+","+str(j_content[i]['useful'])+ ",review" + "\n"

            # RELATION POSTE ET COMMENTE:
            relationposte = relationposte + j_content[i]['user_id']+ "," + j_content[i]['review_id'] + ",poste" + "\n" #Chaine de caractère pour la relation POSTE entre USER et REVIEW
            relationcommente = relationcommente + j_content[i]['review_id']+ "," + j_content[i]['business_id']+ ",commente" + "\n" #Chaine de caractère pour la relation COMMENTE entre REVIEW et RESTAURANT


with open(chemin3) as f:
    for line in f:
        j_content = json.loads(line)
        for i in range(0, len(j_content)):
           #Noeud restaurant
            noeudrestaurant = noeudrestaurant + j_content[i]['business_id'] + "," + (j_content[i]['name'].replace(","," "))+ ",restaurant" + "\n"

           #L'AMBIANCE:
            if j_content[i]['attributes'] is not None and ('Ambience' in j_content[i]['attributes'].keys()): #Si le restaurant à des attributes et contient aussi des ambiances
                ambianceliste=j_content[i]['attributes']['Ambience'].split(',') #Récupérer la liste des ambiances et séparer chaque par chaque ambiance: {u'divey': True
                for h in range (0,len(ambianceliste)-1): #Parcourir la liste des ambiances
                    ambiance=ambianceliste[h].split(':') #Séparer la clée de valeur: {u'divey' OU True
                    if (ambiance[1]== 'True' or 'TRUE'): #Regarde si l'ambiance est présente et donc l'ajouter ensuite
                        ambiancekey=ambiance[0].split("'") #Récuperer jute la partie du nom divey
                        if str(ambiancekey[1]) not in listeambiance: #S'assurer que l'ambiance n'est pas déjà présent
                            listeambiance.append(ambiancekey[1]) #Ajout dans le dictionnaire de l'ambiance et de l'ID

                    # Relation CONTIENT entre NOEUD et AMBIANCE
                    ambiancekey = ambiance[0].split("'")
                    relationcontient = relationcontient + j_content[i]['business_id'] +","+ ambiancekey[1] + ",contient" + "\n"


            #LA CATEGORIE
            categorie = j_content[i]['categories'].split(",")
            for j in (0,len(categorie)-1):
                if categorie[j].lstrip(' ') not in listecategorie:
                    listecategorie.append(categorie[j].lstrip(' '))

                #Relation EST INCLUS entre RESTAURANT et CATEGORIE
                relationestinclus = relationestinclus + j_content[i]['business_id']+","+categorie[j].lstrip(' ')+",estinclus"+"\n"


            #LA GAMME DE PRIX:
            if j_content[i]['attributes'] is not None and ('RestaurantsPriceRange2' in j_content[i]['attributes'].keys()):  # Si le restaurant à des attributes et contient aussi une gamme de prix
                price=j_content[i]['attributes']['RestaurantsPriceRange2']
                if price not in listeprice: # Si le prix n'est pas présent dans le dictionnaire
                    listeprice.append(price)  # Ajout du prix et de l'indice de l'ID

                # Relation PROPOSE entre RESTAURANT et PRICE
                relationpropose = relationpropose+ j_content[i]['business_id'] +","+ price + ",propose" + "\n"

           # LA VILLE
            city=j_content[i]['city'] #Récupérer la ville
            if city not in listecity: #Si la ville n'est pas présente dans le dictionaire
                listecity.append(city) #Ajout de la ville et de l'indice de l'ID

            # Relation SE SITUE entre RESTAURANT et CITY
            relationsesitue= relationsesitue + j_content[i]['business_id'] +","+ city + ",sesitue" + "\n"

#LES NOEUDS:

#Noeud ambiance
for y in range(0,len(listeambiance)):
    noeudambiance=noeudambiance+listeambiance[y]+",ambiance"+"\n"

#Noeud categorie:
for y in range(0,len(listecategorie)):
    noeudcategorie=noeudcategorie+listecategorie[y]+",categorie"+"\n"

#Noeud city:
for y in range(0, len(listecity)):
    noeudcity= noeudcity + listecity[y] + ",city" + "\n"

#Noeud price
for y in range(0, len(listeprice)):
    noeudprice= noeudprice+ listeprice[y] + ",price" + "\n"


#Ecriture dans les fichiers
fichierrelationsesitue.write(relationsesitue)
fichierrelationestinclus.write(relationestinclus)
fichierrelationcontient.write(relationcontient)
fichierrelationpropose.write(relationpropose)
fichiernoeudrestaurant.write(noeudrestaurant)
fichiernoeudcity.write(noeudcity)
fichiernoeudcategorie.write(noeudcategorie)
fichiernoeudambiance.write(noeudambiance)
fichiernoeudprice.write(noeudprice)
fichiernrelationfriends.write(relationfriends)
fichiernrelationdata.write(relationdata)
fichiernoeuduser.write(noeuduser)
fichiernoeuddata.write(noeudata)
fichiernoeudreview.write(noeudreview)
fichierrelationposte.write(relationposte)
fichierrelationcommente.write(relationcommente)



print('execution Terminée !!')
