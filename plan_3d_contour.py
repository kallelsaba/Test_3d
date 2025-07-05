import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def creer_plan_3d():
    """
    Génère une version 3D du plan architectural en forme de croix
    """
    print("=== Générateur de Plan 3D ===")
    
    # Saisie des paramètres
    try:
        # Dimensions de la structure en croix
        largeur_centrale = float(input("Entrez la largeur de la partie centrale: "))
        longueur_centrale = float(input("Entrez la longueur de la partie centrale: "))
        largeur_bras = float(input("Entrez la largeur des bras de la croix: "))
        longueur_bras = float(input("Entrez la longueur des bras de la croix: "))
        hauteur = float(input("Entrez la hauteur du bâtiment: "))
        
        if any(val <= 0 for val in [largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, hauteur]):
            print("Erreur: Toutes les valeurs doivent être positives!")
            return
            
    except ValueError:
        print("Erreur: Veuillez entrer des nombres valides!")
        return
    
    # Création de la figure 3D
    fig = plt.figure(figsize=(15, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Générer la structure 3D
    generer_structure_croix(ax, largeur_centrale, longueur_centrale, 
                           largeur_bras, longueur_bras, hauteur)
    
    # Configuration de l'affichage
    ax.set_xlabel('X (Largeur)')
    ax.set_ylabel('Y (Longueur)')
    ax.set_zlabel('Z (Hauteur)')
    ax.set_title('Plan Architectural 3D - Structure en Croix')
    
    # Égaliser les échelles des axes
    max_dim = max(largeur_centrale + 2*longueur_bras, longueur_centrale + 2*longueur_bras, hauteur)
    ax.set_xlim([0, max_dim])
    ax.set_ylim([0, max_dim])
    ax.set_zlim([0, hauteur])
    
    # Améliorer la vue
    ax.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.show()

def generer_structure_croix(ax, largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, hauteur):
    """
    Génère la structure en forme de croix avec uniquement les contours extérieurs (plan vide à l'intérieur)
    """
    # Calcul des dimensions totales
    largeur_totale = largeur_centrale + 2 * longueur_bras
    longueur_totale = longueur_centrale + 2 * longueur_bras
    
    # Centre de la structure
    centre_x = largeur_totale / 2
    centre_y = longueur_totale / 2
    
    # Dessiner uniquement le contour extérieur de la forme en croix
    dessiner_contour_croix(ax, centre_x, centre_y, largeur_centrale, longueur_centrale,
                          largeur_bras, longueur_bras, hauteur)

def dessiner_contour_croix(ax, centre_x, centre_y, largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, hauteur):
    """
    Dessine uniquement le contour extérieur de la forme en croix (plan vide à l'intérieur)
    """
    # Définir tous les points du contour extérieur de la croix
    # En partant du coin inférieur gauche et en tournant dans le sens horaire
    
    # Points de base (z=0) du contour extérieur
    points_base = []
    
    # Partir du coin inférieur gauche du bras gauche
    x_start = centre_x - largeur_centrale/2 - longueur_bras
    y_start = centre_y - largeur_bras/2
    
    # Contour extérieur de la croix (base z=0)
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

def menu_principal():
    """
    Menu principal du programme
    """
    while True:
        print("\n" + "="*50)
        print("    GÉNÉRATEUR DE PLAN ARCHITECTURAL 3D")
        print("="*50)
        print("1. Générer un plan 3D en forme de croix")
        print("2. Quitter")
        
        choix = input("\nVotre choix (1-2): ").strip()
        
        if choix == "1":
            creer_plan_3d()
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
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        menu_principal()
    except ImportError:
        print("Erreur: matplotlib n'est pas installé!")
        print("Installez-le avec: pip install matplotlib")