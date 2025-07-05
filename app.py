import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def dessiner_parallelepipede_avec_spheres():
    """
    Génère et affiche un parallélépipède rectangle rempli de sphères
    """
    print("=== Générateur de Parallélépipède avec Sphères ===")
    
    # Saisie des dimensions du parallélépipède
    try:
        largeur = float(input("Entrez la largeur du parallélépipède (axe X): "))
        longueur = float(input("Entrez la longueur du parallélépipède (axe Y): "))
        hauteur = float(input("Entrez la hauteur du parallélépipède (axe Z): "))
        rayon_sphere = float(input("Entrez le rayon des sphères: "))
        
        if largeur <= 0 or longueur <= 0 or hauteur <= 0 or rayon_sphere <= 0:
            print("Erreur: Toutes les valeurs doivent être positives!")
            return
            
        if rayon_sphere * 2 > min(largeur, longueur, hauteur):
            print("Attention: Le diamètre des sphères est plus grand que la plus petite dimension!")
            
    except ValueError:
        print("Erreur: Veuillez entrer des nombres valides!")
        return
    
    # Calcul du nombre de sphères dans chaque direction
    # On calcule combien de sphères peuvent tenir dans chaque dimension
    # en gardant un espacement minimal égal au diamètre pour éviter les chevauchements
    diametre = 2 * rayon_sphere
    
    # Calcul du nombre maximal de sphères par dimension
    # On s'assure qu'il y a assez d'espace pour placer les sphères sans qu'elles dépassent
    nx = max(1, int(largeur / diametre))
    ny = max(1, int(longueur / diametre))
    nz = max(1, int(hauteur / diametre))
    
    # Vérification que les sphères peuvent physiquement tenir dans l'espace
    espace_min_x = largeur / nx
    espace_min_y = longueur / ny
    espace_min_z = hauteur / nz
    
    if (espace_min_x < diametre or espace_min_y < diametre or espace_min_z < diametre):
        print("Attention: Les sphères risquent de se chevaucher!")
    
    print(f"\nNombre de sphères: {nx} x {ny} x {nz} = {nx * ny * nz} sphères")
    print(f"Espace alloué par sphère: {espace_min_x:.1f} x {espace_min_y:.1f} x {espace_min_z:.1f}")
    
    # Création de la figure 3D
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # Génération des centres des sphères
    centres_x = []
    centres_y = []
    centres_z = []
    
    # Calcul des positions pour centrer les sphères dans des sous-volumes égaux
    # Diviser chaque dimension en nx, ny, nz parties égales
    # Placer chaque sphère au centre de gravité de son sous-volume
    
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                # Calculer le centre de chaque sous-volume
                # Chaque sous-volume a une largeur de largeur/nx, longueur/ny, hauteur/nz
                x = (i + 0.5) * (largeur / nx)  # Centre en X du sous-volume i
                y = (j + 0.5) * (longueur / ny)  # Centre en Y du sous-volume j
                z = (k + 0.5) * (hauteur / nz)  # Centre en Z du sous-volume k
                
                centres_x.append(x)
                centres_y.append(y)
                centres_z.append(z)
    
    # Dessiner le contour du parallélépipède
    dessiner_contour_parallelepipede(ax, largeur, longueur, hauteur)
    
    # Dessiner les sphères
    dessiner_spheres(ax, centres_x, centres_y, centres_z, rayon_sphere)
    
    # Configuration de l'affichage
    ax.set_xlabel('X (Largeur)')
    ax.set_ylabel('Y (Longueur)')
    ax.set_zlabel('Z (Hauteur)')
    ax.set_title(f'Parallélépipède ({largeur}x{longueur}x{hauteur}) avec {len(centres_x)} sphères (r={rayon_sphere})')
    
    # Égaliser les échelles des axes
    max_dim = max(largeur, longueur, hauteur)
    ax.set_xlim([0, max_dim])
    ax.set_ylim([0, max_dim])
    ax.set_zlim([0, max_dim])
    
    # Informations supplémentaires
    volume_parallelepipede = largeur * longueur * hauteur
    volume_sphere = (4/3) * np.pi * rayon_sphere**3
    volume_total_spheres = len(centres_x) * volume_sphere
    taux_remplissage = (volume_total_spheres / volume_parallelepipede) * 100
    
    print(f"\n=== Statistiques ===")
    print(f"Volume du parallélépipède: {volume_parallelepipede:.2f}")
    print(f"Volume d'une sphère: {volume_sphere:.2f}")
    print(f"Volume total des sphères: {volume_total_spheres:.2f}")
    print(f"Taux de remplissage: {taux_remplissage:.1f}%")
    
    plt.tight_layout()
    plt.show()

def dessiner_contour_parallelepipede(ax, largeur, longueur, hauteur):
    """
    Dessine le contour du parallélépipède
    """
    # Définir les 8 sommets du parallélépipède
    sommets = np.array([
        [0, 0, 0], [largeur, 0, 0], [largeur, longueur, 0], [0, longueur, 0],  # base inférieure
        [0, 0, hauteur], [largeur, 0, hauteur], [largeur, longueur, hauteur], [0, longueur, hauteur]  # base supérieure
    ])
    
    # Définir les arêtes du parallélépipède
    aretes = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # base inférieure
        [4, 5], [5, 6], [6, 7], [7, 4],  # base supérieure
        [0, 4], [1, 5], [2, 6], [3, 7]   # arêtes verticales
    ]
    
    # Dessiner les arêtes
    for arete in aretes:
        points = sommets[arete]
        ax.plot3D(*points.T, 'k-', linewidth=2, alpha=0.6)

def dessiner_spheres(ax, centres_x, centres_y, centres_z, rayon):
    """
    Dessine les sphères dans le repère 3D
    """
    # Créer une sphère unitaire
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 15)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Dessiner chaque sphère
    colors = plt.cm.viridis(np.linspace(0, 1, len(centres_x)))
    
    for i, (cx, cy, cz) in enumerate(zip(centres_x, centres_y, centres_z)):
        # Adapter la taille et la position de la sphère
        x = rayon * x_sphere + cx
        y = rayon * y_sphere + cy
        z = rayon * z_sphere + cz
        
        # Dessiner la sphère avec une couleur différente
        ax.plot_surface(x, y, z, color=colors[i], alpha=0.7, linewidth=0)

def menu_principal():
    """
    Menu principal du programme
    """
    while True:
        print("\n" + "="*50)
        print("    GÉNÉRATEUR DE PARALLÉLÉPIPÈDE AVEC SPHÈRES")
        print("="*50)
        print("1. Générer un nouveau parallélépipède")
        print("2. Quitter")
        
        choix = input("\nVotre choix (1-2): ").strip()
        
        if choix == "1":
            dessiner_parallelepipede_avec_spheres()
        elif choix == "2":
            print("Au revoir!")
            break
        else:
            print("Choix invalide! Veuillez entrer 1 ou 2.")

if __name__ == "__main__":
    # Vérifier que matplotlib est disponible
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        menu_principal()
    except ImportError:
        print("Erreur: matplotlib n'est pas installé!")
        print("Installez-le avec: pip install matplotlib")