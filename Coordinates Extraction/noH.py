import csv

def retirer_colonnes_hydrogene_amber(fichier_entree, fichier_sortie):
    # Motifs AMBER pour les noms d'atomes d'hydrogène
    motifs_hydrogene = [
        "H1", "H2", "H3", "HA", "HB", "HC", "HD", "HE", "HH", "HG", "HP", "HZ","HS","Hx","Hy","Hz"
        # Ajoutez d'autres motifs spécifiques AMBER si nécessaire
    ]
    
    # Lire le fichier CSV et identifier les colonnes à garder
    with open(fichier_entree, mode='r', newline='') as csvfile:
        lecteur_csv = csv.reader(csvfile)
        # Lire l'en-tête
        entetes = next(lecteur_csv)

        # Identifier les colonnes qui ne contiennent pas de motifs d'hydrogène
        colonnes_a_garder = [
            index for index, col in enumerate(entetes) 
            if not any(motif in col for motif in motifs_hydrogene)
        ]

        # Écrire le fichier filtré
        with open(fichier_sortie, mode='w', newline='') as fichier_filtre:
            ecrivain_csv = csv.writer(fichier_filtre)

            # Écrire l'en-tête filtrée
            entetes_filtrees = [entetes[i] for i in colonnes_a_garder]
            ecrivain_csv.writerow(entetes_filtrees)

            # Filtrer et écrire les autres lignes
            for ligne in lecteur_csv:
                ligne_filtre = [ligne[i] for i in colonnes_a_garder]
                ecrivain_csv.writerow(ligne_filtre)

    print(f"Les colonnes contenant des atomes d'hydrogène (codes AMBER) ont été supprimées. Fichier de sortie: {fichier_sortie}")

# Exemple d'utilisation
fichier_entree = "output_coordinates.csv"
fichier_sortie = "NoH.csv"
retirer_colonnes_hydrogene_amber(fichier_entree, fichier_sortie)

