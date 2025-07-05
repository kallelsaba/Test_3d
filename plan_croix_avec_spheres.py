import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def creer_plan_croix_avec_spheres():
    """
    Génère un plan 3D en forme de croix rempli de sphères
    """
    print("=== Générateur de Plan en Croix avec Sphères ===")
    
    # Saisie des paramètres
    try:
        # Dimensions de la structure en croix
        largeur_centrale = float(input("Entrez la largeur de la partie centrale: "))
        longueur_centrale = float(input("Entrez la longueur de la partie centrale: "))
        largeur_bras = float(input("Entrez la largeur des bras de la croix: "))
        longueur_bras = float(input("Entrez la longueur des bras de la croix: "))
        hauteur = float(input("Entrez la hauteur du bâtiment: "))
        rayon_sphere = float(input("Entrez le rayon des sphères: "))
        
        if any(val <= 0 for val in [largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, hauteur, rayon_sphere]):
            print("Erreur: Toutes les valeurs doivent être positives!")
            return
            
    except ValueError:
        print("Erreur: Veuillez entrer des nombres valides!")
        return
    
    # Création de la figure 3D
    fig = plt.figure(figsize=(15, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Générer la structure avec sphères
    centres_x, centres_y, centres_z = generer_spheres_dans_croix(
        largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, hauteur, rayon_sphere)
    
    # Dessiner le contour de la croix
    dessiner_contour_croix_3d(ax, largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, hauteur)
    
    # Dessiner les sphères
    dessiner_spheres(ax, centres_x, centres_y, centres_z, rayon_sphere)
    
    # Configuration de l'affichage
    ax.set_xlabel('X (Largeur)')
    ax.set_ylabel('Y (Longueur)')
    ax.set_zlabel('Z (Hauteur)')
    ax.set_title(f'Plan en Croix avec {len(centres_x)} sphères (r={rayon_sphere})')
    
    # Égaliser les échelles des axes
    largeur_totale = largeur_centrale + 2 * longueur_bras
    longueur_totale = longueur_centrale + 2 * longueur_bras
    max_dim = max(largeur_totale, longueur_totale, hauteur)
    ax.set_xlim([0, max_dim])
    ax.set_ylim([0, max_dim])
    ax.set_zlim([0, hauteur])
    
    # Améliorer la vue
    ax.view_init(elev=30, azim=45)
    
    # Statistiques
    volume_croix = calculer_volume_croix(largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, hauteur)
    volume_sphere = (4/3) * np.pi * rayon_sphere**3
    volume_total_spheres = len(centres_x) * volume_sphere
    taux_remplissage = (volume_total_spheres / volume_croix) * 100
    
    print(f"\n=== Statistiques ===")
    print(f"Volume de la structure en croix: {volume_croix:.2f}")
    print(f"Volume d'une sphère: {volume_sphere:.2f}")
    print(f"Volume total des sphères: {volume_total_spheres:.2f}")
    print(f"Taux de remplissage: {taux_remplissage:.1f}%")
    
    plt.tight_layout()
    plt.show()

def generer_spheres_dans_croix(largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, hauteur, rayon_sphere):
    """
    Génère les positions des sphères dans les différentes parties de la croix
    """
    centres_x = []
    centres_y = []
    centres_z = []
    
    # Calcul des dimensions totales
    largeur_totale = largeur_centrale + 2 * longueur_bras
    longueur_totale = longueur_centrale + 2 * longueur_bras
    
    # Centre de la structure
    centre_x = largeur_totale / 2
    centre_y = longueur_totale / 2
    
    diametre = 2 * rayon_sphere
    
    # 1. PARTIE CENTRALE
    centres_partie = generer_spheres_rectangle(
        centre_x - largeur_centrale/2, centre_y - longueur_centrale/2,
        largeur_centrale, longueur_centrale, hauteur, diametre
    )
    centres_x.extend([c[0] for c in centres_partie])
    centres_y.extend([c[1] for c in centres_partie])
    centres_z.extend([c[2] for c in centres_partie])
    
    # 2. BRAS GAUCHE
    centres_bras = generer_spheres_rectangle(
        centre_x - largeur_centrale/2 - longueur_bras, centre_y - largeur_bras/2,
        longueur_bras, largeur_bras, hauteur, diametre
    )
    centres_x.extend([c[0] for c in centres_bras])
    centres_y.extend([c[1] for c in centres_bras])
    centres_z.extend([c[2] for c in centres_bras])
    
    # 3. BRAS DROIT
    centres_bras = generer_spheres_rectangle(
        centre_x + largeur_centrale/2, centre_y - largeur_bras/2,
        longueur_bras, largeur_bras, hauteur, diametre
    )
    centres_x.extend([c[0] for c in centres_bras])
    centres_y.extend([c[1] for c in centres_bras])
    centres_z.extend([c[2] for c in centres_bras])
    
    # 4. BRAS HAUT
    centres_bras = generer_spheres_rectangle(
        centre_x - largeur_bras/2, centre_y + longueur_centrale/2,
        largeur_bras, longueur_bras, hauteur, diametre
    )
    centres_x.extend([c[0] for c in centres_bras])
    centres_y.extend([c[1] for c in centres_bras])
    centres_z.extend([c[2] for c in centres_bras])
    
    # 5. BRAS BAS
    centres_bras = generer_spheres_rectangle(
        centre_x - largeur_bras/2, centre_y - longueur_centrale/2 - longueur_bras,
        largeur_bras, longueur_bras, hauteur, diametre
    )
    centres_x.extend([c[0] for c in centres_bras])
    centres_y.extend([c[1] for c in centres_bras])
    centres_z.extend([c[2] for c in centres_bras])
    
    print(f"Nombre total de sphères générées: {len(centres_x)}")
    
    return centres_x, centres_y, centres_z

def generer_spheres_rectangle(x_start, y_start, largeur, longueur, hauteur, diametre):
    """
    Génère les positions des sphères dans un rectangle donné
    """
    centres = []
    
    # Calcul du nombre de sphères par dimension
    nx = max(1, int(largeur / diametre))
    ny = max(1, int(longueur / diametre))
    nz = max(1, int(hauteur / diametre))
    
    print(f"Rectangle ({largeur:.1f}x{longueur:.1f}x{hauteur:.1f}): {nx}x{ny}x{nz} = {nx*ny*nz} sphères")
    
    # Génération des positions centrées dans chaque sous-volume
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                x = x_start + (i + 0.5) * (largeur / nx)
                y = y_start + (j + 0.5) * (longueur / ny)
                z = (k + 0.5) * (hauteur / nz)
                centres.append([x, y, z])
    
    return centres

def dessiner_contour_croix_3d(ax, largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, hauteur):
    """
    Dessine le contour 3D de la structure en croix
    """
    # Calcul des dimensions totales
    largeur_totale = largeur_centrale + 2 * longueur_bras
    longueur_totale = longueur_centrale + 2 * longueur_bras
    
    # Centre de la structure
    centre_x = largeur_totale / 2
    centre_y = longueur_totale / 2
    
    # Définir tous les points du contour extérieur de la croix
    x_start = centre_x - largeur_centrale/2 - longueur_bras
    y_start = centre_y - largeur_bras/2
    
    # Points de base (z=0) du contour extérieur
    points_base = [
        # Bras gauche - partie basse
        [x_start, y_start, 0],
        [x_start + longueur_bras, y_start, 0],
        
        # Partie centrale - côté gauche bas
        [centre_x - largeur_centrale/2, y_start, 0],
        [centre_x - largeur_centrale/2, centre_y - longueur_centrale/2, 0],
        
        # Bras bas
        [centre_x - largeur_bras/2, centre_y - longueur_centrale/2, 0],
        [centre_x - largeur_bras/2, centre_y - longueur_centrale/2 - longueur_bras, 0],
        [centre_x + largeur_bras/2, centre_y - longueur_centrale/2 - longueur_bras, 0],
        [centre_x + largeur_bras/2, centre_y - longueur_centrale/2, 0],
        
        # Partie centrale - côté droit bas
        [centre_x + largeur_centrale/2, centre_y - longueur_centrale/2, 0],
        [centre_x + largeur_centrale/2, y_start, 0],
        
        # Bras droit - partie basse
        [centre_x + largeur_centrale/2 + longueur_bras, y_start, 0],
        [centre_x + largeur_centrale/2 + longueur_bras, y_start + largeur_bras, 0],
        
        # Bras droit - partie haute
        [centre_x + largeur_centrale/2, y_start + largeur_bras, 0],
        [centre_x + largeur_centrale/2, centre_y + longueur_centrale/2, 0],
        
        # Bras haut
        [centre_x + largeur_bras/2, centre_y + longueur_centrale/2, 0],
        [centre_x + largeur_bras/2, centre_y + longueur_centrale/2 + longueur_bras, 0],
        [centre_x - largeur_bras/2, centre_y + longueur_centrale/2 + longueur_bras, 0],
        [centre_x - largeur_bras/2, centre_y + longueur_centrale/2, 0],
        
        # Partie centrale - côté gauche haut
        [centre_x - largeur_centrale/2, centre_y + longueur_centrale/2, 0],
        [centre_x - largeur_centrale/2, y_start + largeur_bras, 0],
        
        # Retour au point de départ
        [x_start, y_start + largeur_bras, 0]
    ]
    
    # Créer les points du sommet (même contour mais à z=hauteur)
    points_sommet = [[p[0], p[1], hauteur] for p in points_base]
    
    # Dessiner le contour de base (z=0)
    for i in range(len(points_base)):
        j = (i + 1) % len(points_base)
        ax.plot3D([points_base[i][0], points_base[j][0]], 
                  [points_base[i][1], points_base[j][1]], 
                  [points_base[i][2], points_base[j][2]], 
                  color='black', linewidth=2)
    
    # Dessiner le contour du sommet (z=hauteur)
    for i in range(len(points_sommet)):
        j = (i + 1) % len(points_sommet)
        ax.plot3D([points_sommet[i][0], points_sommet[j][0]], 
                  [points_sommet[i][1], points_sommet[j][1]], 
                  [points_sommet[i][2], points_sommet[j][2]], 
                  color='black', linewidth=2)
    
    # Dessiner les arêtes verticales
    for i in range(len(points_base)):
        ax.plot3D([points_base[i][0], points_sommet[i][0]], 
                  [points_base[i][1], points_sommet[i][1]], 
                  [points_base[i][2], points_sommet[i][2]], 
                  color='black', linewidth=2)

def dessiner_spheres(ax, centres_x, centres_y, centres_z, rayon):
    """
    Dessine les sphères dans le repère 3D
    """
    # Créer une sphère unitaire
    u = np.linspace(0, 2 * np.pi, 15)
    v = np.linspace(0, np.pi, 10)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Dessiner chaque sphère avec une couleur basée sur la hauteur
    z_min, z_max = min(centres_z), max(centres_z)
    
    for i, (cx, cy, cz) in enumerate(zip(centres_x, centres_y, centres_z)):
        # Adapter la taille et la position de la sphère
        x = rayon * x_sphere + cx
        y = rayon * y_sphere + cy
        z = rayon * z_sphere + cz
        
        # Couleur basée sur la hauteur
        if z_max > z_min:
            color_intensity = (cz - z_min) / (z_max - z_min)
        else:
            color_intensity = 0.5
        
        color = plt.cm.viridis(color_intensity)
        
        # Dessiner la sphère
        ax.plot_surface(x, y, z, color=color, alpha=0.7, linewidth=0)

def calculer_volume_croix(largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, hauteur):
    """
    Calcule le volume total de la structure en croix
    """
    # Volume de la partie centrale
    volume_central = largeur_centrale * longueur_centrale * hauteur
    
    # Volume des 4 bras
    volume_bras = 4 * (longueur_bras * largeur_bras * hauteur)
    
    return volume_central + volume_bras

def menu_principal():
    """
    Menu principal du programme
    """
    while True:
        print("\n" + "="*60)
        print("    GÉNÉRATEUR DE PLAN EN CROIX AVEC SPHÈRES")
        print("="*60)
        print("1. Générer un plan en croix rempli de sphères")
        print("2. Quitter")
        
        choix = input("\nVotre choix (1-2): ").strip()
        
        if choix == "1":
            creer_plan_croix_avec_spheres()
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
