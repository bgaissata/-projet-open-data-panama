import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain
import numpy as np

# Charger les données des fichiers nodes et edges
nodes_file = "panama_papers_project/data/All-nodes.csv"
edges_file = "panama_papers_project/data/All-edges.csv"

# Charger les fichiers CSV
nodes_df = pd.read_csv(nodes_file)
edges_df = pd.read_csv(edges_file)

# Afficher les premières lignes pour voir les données et vérifier les colonnes
print("Affichage des premières lignes du fichier nodes :")
print(nodes_df.head())
print("Affichage des premières lignes du fichier edges :")
print(edges_df.head())

# Créer un graphe vide
G = nx.Graph()

# Vérification des valeurs uniques dans la colonne 'data.categories.0' pour voir les types
print("Valeurs uniques dans 'data.categories.0' :")
print(nodes_df['data.categories.0'].unique())

# Ajouter les nœuds au graphe
for index, row in nodes_df.iterrows():
    G.add_node(row['id'], label=row['label'])  # Assurez-vous d'ajuster les noms de colonnes

# Ajouter les arêtes avec un affichage des types de nœuds
for index, row in edges_df.iterrows():
    source_node = row['source']
    target_node = row['target']
    
    # Récupérer les types des nœuds source et target
    source_type = nodes_df.loc[nodes_df['id'] == source_node, 'data.categories.0'].values[0]
    target_type = nodes_df.loc[nodes_df['id'] == target_node, 'data.categories.0'].values[0]
    
    # Affichage des types de source et target pour débogage
    print(f"source_type: {source_type}, target_type: {target_type}")
    
    # Vérification du filtre pour les arêtes entre 'person' et 'company'
    if (source_type == 'person' and target_type == 'company') or (source_type == 'company' and target_type == 'person'):
        G.add_edge(source_node, target_node)
    else:
        print(f"Arête ignorée entre {source_node} et {target_node} car les types ne correspondent.")

# Vérification de la création du graphe
print(f"Le graphe contient {len(G.nodes)} nœuds et {len(G.edges)} arêtes.")

# Optionnel : ajouter les arêtes sans condition pour voir si des liens existent
print("\nAjout de toutes les arêtes sans condition pour tester la connectivité du graphe.")
for index, row in edges_df.iterrows():
    source_node = row['source']
    target_node = row['target']
    G.add_edge(source_node, target_node)  # Ajoute toutes les arêtes sans condition

# Vérification : Afficher quelques arêtes ajoutées
print("\nQuelques arêtes ajoutées dans le graphe :")
for edge in list(G.edges)[:5]:
    print(edge)

# Détection des communautés avec la méthode Louvain
partition = community_louvain.best_partition(G)

# Calcul du nombre initial de communautés
current_community_count = len(set(partition.values()))
print(f"Nombre initial de communautés : {current_community_count}")

# Forcer 50 communautés
target_community_count = 50
if current_community_count > target_community_count:
    # Si le nombre de communautés est supérieur à 50, fusionner les communautés
    community_list = list(set(partition.values()))
    new_partition = {}
    for i, node in enumerate(G.nodes):
        # Assigner des communautés de manière circulaire pour obtenir 50 communautés
        new_partition[node] = community_list[i % target_community_count]
    partition = new_partition
elif current_community_count < target_community_count:
    # Si le nombre de communautés est inférieur à 50, créer des communautés supplémentaires
    additional_communities = target_community_count - current_community_count
    new_partition = partition.copy()
    new_community_start = current_community_count
    for i, node in enumerate(G.nodes):
        if new_partition[node] == current_community_count - 1:
            new_partition[node] = new_community_start
            new_community_start += 1
        else:
            new_partition[node] = current_community_count - 1
    partition = new_partition

# Ajouter l'attribut 'community' à chaque nœud du graphe
for node, community_id in partition.items():
    G.nodes[node]['community'] = community_id

# Vérification : Afficher les 5 premiers nœuds avec leurs communautés
for node in list(G.nodes)[:5]:
    print(f"Nœud {node}, Communauté: {G.nodes[node].get('community')}")
# Affichage du graphe pour une sélection de 30 nœuds
plt.figure(figsize=(10, 10))
subgraph_nodes = list(G.nodes)[:30]  # Choisir les 30 premiers nœuds
subgraph = G.subgraph(subgraph_nodes)
pos = nx.spring_layout(subgraph)

# Dessiner le sous-graphe avec les communautés
community_colors = [G.nodes[node]['community'] for node in subgraph_nodes]
node_color_map = plt.cm.rainbow(np.linspace(0, 1, len(set(community_colors))))  # Génère une palette de couleurs

# Afficher le sous-graphe
nx.draw(subgraph, pos, node_color=community_colors, with_labels=True, node_size=500, font_size=8, cmap=plt.cm.rainbow)

# Ajouter une légende pour les communautés
handles = []
for i, community in enumerate(set(community_colors)):
    handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=node_color_map[i], markersize=10))

# Positionner la légende à l'extérieur du graphe
plt.legend(handles=handles, labels=[f'Communauté {i}' for i in range(len(set(community_colors)))], title="Communautés", loc='upper left', bbox_to_anchor=(1, 1))

# Titre et sauvegarde de l'image
plt.title("Sous-graphe avec communautés")
plt.savefig("graph_subgraph_communities_with_edges_and_legend.png", format="PNG", dpi=300, bbox_inches='tight')

# Optionnel : pour sauvegarder en PDF, décommenter la ligne suivante :
# plt.savefig("graph_subgraph_communities.pdf", format="PDF", bbox_inches='tight')


# Affichage des communautés détectées
print("Communautés détectées (jusqu'à 50) :")
num_communities = len(set(partition.values()))
for i in range(num_communities):
    community_nodes = [node for node, data in G.nodes(data=True) if data['community'] == i]
    print(f"Communauté {i}: {community_nodes[:5]}...")  # Afficher les 5 premiers nœuds de chaque communauté pour un aperçu
