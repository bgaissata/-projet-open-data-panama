import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Charger les données des fichiers nodes et edges
nodes_file = "panama_papers_project/data/All-nodes.csv"
edges_file = "panama_papers_project/data/All-edges.csv"

# Charger les fichiers CSV
nodes_df = pd.read_csv(nodes_file)
edges_df = pd.read_csv(edges_file)

# Créer un graphe vide
G = nx.Graph()

# Ajouter les nœuds au graphe
for index, row in nodes_df.iterrows():
    G.add_node(row['id'], label=row['label'])  # Assurez-vous d'ajuster les noms de colonnes

# Ajouter les arêtes sans condition
for index, row in edges_df.iterrows():
    source_node = row['source']
    target_node = row['target']
    G.add_edge(source_node, target_node)  # Ajoute toutes les arêtes sans condition

# Vérification : Afficher quelques arêtes ajoutées
print("\nQuelques arêtes ajoutées dans le graphe :")
for edge in list(G.edges)[:5]:
    print(edge)

# Vérification de la création du graphe
print(f"Le graphe contient {len(G.nodes)} nœuds et {len(G.edges)} arêtes.")

# Affichage du graphe pour une sélection de 50 nœuds
plt.figure(figsize=(15, 15))  # Taille de la figure plus grande

# Sélectionner les 50 premiers nœuds pour l'affichage
subgraph_nodes = list(G.nodes)[:50]
subgraph = G.subgraph(subgraph_nodes)
pos = nx.kamada_kawai_layout(subgraph)  # Utiliser le layout Kamada-Kawai pour l'affichage

# Dessiner le sous-graphe avec les 50 premiers nœuds
nx.draw(subgraph, pos, with_labels=True, node_size=600, font_size=10, node_color='skyblue', font_color='black', edge_color='gray')

# Titre et sauvegarde de l'image
plt.title("Graphe complet sans communautés avec Kamada-Kawai Layout (50 nœuds)")
plt.savefig("graph_complete_without_communities_50_nodes.png", format="PNG", dpi=300)

# Affichage d'un message pour indiquer que l'image a été sauvegardée
print("Le graphe complet sans communautés avec 50 nœuds a été sauvegardé sous 'graph_complete_without_communities_50_nodes.png'.")
