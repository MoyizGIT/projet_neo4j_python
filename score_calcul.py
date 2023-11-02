import multiprocessing
import numpy as np
from py2neo import Graph
import pandas as pd
import multiprocess
import time

# Configuration de la connexion Neo4j
neo = Graph("bolt://localhost:7687", auth=("neo4j", "123"))

# Définition de fonctions pour récupérer des données des utilisateurs

def get_users_by_price(price):
    price = f'"{price}"'
    cypher = f"MATCH (:price{{price:{price}}})<-[:propose]-(:restaurant)-[:commente]-(:review)-[:poste]-(n:user) RETURN n.name AS Utilisateur, n.user AS Id"
    return neo.run(cypher).to_data_frame()

def get_users_by_city(city):
    city = f'"{city}"'
    cypher = f"MATCH (:city{{city:{city}}})<-[:sesitue]-(restaurant)-[:commente]-(:review)-[:poste]-(n:user) RETURN n.name AS Utilisateur, n.user AS Id"
    return neo.run(cypher).to_data_frame()

def get_users_by_criteria(criteria_list, label, relationship_type, label_name):
    users = pd.DataFrame(columns=['Utilisateur', 'Id'])
    for criteria in criteria_list:
        criteria = f'"{criteria}"'
        cypher = f"MATCH (:{label}{{ {label_name}:{criteria} }})<-[:{relationship_type}]-(restaurant)-[:commente]-(:review)-[:poste]-(n:user) RETURN n.name AS Utilisateur, n.user AS Id"
        users = users.append(neo.run(cypher).to_data_frame(), ignore_index=True)
    users = users.drop_duplicates(subset="Id")
    return users

# Définition de fonctions pour calculer les scores

def calculate_social_score(users, max_score_query, score_query):
    max_score = neo.run(max_score_query).to_data_frame().iloc[0, 0]
    users_scores = neo.run(score_query).to_data_frame()
    users_scores['Score'] = users_scores.apply(lambda row: row['Score'] / max_score if max_score != 0 else 0, axis=1)
    return users_scores

def calculate_validity_score(users, max_score_query, score_query):
    max_score = neo.run(max_score_query).to_data_frame().iloc[0, 0]
    users_scores = neo.run(score_query).to_data_frame()
    users_scores['Score'] = users_scores.apply(lambda row: row['Score'] / max_score if max_score != 0 else 0, axis=1)
    return users_scores

# ... Ajouter d'autres fonctions pour calculer les scores des autres facteurs ...

def main_recommendation(ambiance_list, categorie_list, ville, prix):
    users_by_price = get_users_by_price(prix)
    users_by_city = get_users_by_city(ville)
    users_by_ambiance = get_users_by_criteria(ambiance_list, "ambiance", "contient", "ambiance")
    users_by_categorie = get_users_by_criteria(categorie_list, "categorie", "estinclus", "categorie")
    
    # Combinez les utilisateurs en fonction de vos critères
    combined_users = users_by_price.merge(users_by_city, on="Id").merge(users_by_ambiance, on="Id").merge(users_by_categorie, on="Id")
    
    # ... Calculez les scores d'autres facteurs ...
    
    # Calculez le score final
    combined_users['Total'] = (
        (combined_users['SocialScore'] * 0.3 +
         combined_users['ValidityScore'] * 0.3 +
         combined_users['OtherFactorScore'] * 0.3 +
         combined_users['AnotherFactorScore'] * 0.1)
    )
    
    # Triez les utilisateurs par score
    top_influencers = combined_users.sort_values(by='Total', ascending=False).head(10)
    
    # Affichez les meilleurs influenceurs
    print("Le TOP 10 DES INFLUENCEURS:")
    print(top_influencers[['Utilisateur', 'Id', 'Total']])

if __name__ == '__main__':
    # ... Lire les critères de l'utilisateur et lancez la recommandation ...
