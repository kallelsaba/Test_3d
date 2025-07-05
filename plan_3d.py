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
        epaisseur_mur = float(input("Entrez l'épaisseur des murs: "))
        
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
                           largeur_bras, longueur_bras, hauteur, epaisseur_mur)
    
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

def generer_structure_croix(ax, largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, hauteur, epaisseur_mur):
    """
    Génère la structure en forme de croix avec des murs en 3D
    """
    # Couleurs pour différentes parties
    couleur_mur_ext = 'lightblue'
    couleur_mur_int = 'lightgray'
    couleur_sol = 'beige'
    
    # Calcul des dimensions totales
    largeur_totale = largeur_centrale + 2 * longueur_bras
    longueur_totale = longueur_centrale + 2 * longueur_bras
    
    # Centre de la structure
    centre_x = largeur_totale / 2
    centre_y = longueur_totale / 2
    
    # 1. PARTIE CENTRALE (rectangle central)
    # Murs extérieurs de la partie centrale
    dessiner_rectangle_3d(ax, 
                         centre_x - largeur_centrale/2, centre_y - longueur_centrale/2,
                         largeur_centrale, longueur_centrale, hauteur, epaisseur_mur,
                         couleur_mur_ext, "Partie centrale")
    
    # 2. BRAS HORIZONTAL (gauche et droite)
    # Bras gauche
    dessiner_rectangle_3d(ax,
                         centre_x - largeur_centrale/2 - longueur_bras, centre_y - largeur_bras/2,
                         longueur_bras, largeur_bras, hauteur, epaisseur_mur,
                         couleur_mur_ext, "Bras gauche")
    
    # Bras droit
    dessiner_rectangle_3d(ax,
                         centre_x + largeur_centrale/2, centre_y - largeur_bras/2,
                         longueur_bras, largeur_bras, hauteur, epaisseur_mur,
                         couleur_mur_ext, "Bras droit")
    
    # 3. BRAS VERTICAL (haut et bas)
    # Bras haut
    dessiner_rectangle_3d(ax,
                         centre_x - largeur_bras/2, centre_y + longueur_centrale/2,
                         largeur_bras, longueur_bras, hauteur, epaisseur_mur,
                         couleur_mur_ext, "Bras haut")
    
    # Bras bas
    dessiner_rectangle_3d(ax,
                         centre_x - largeur_bras/2, centre_y - longueur_centrale/2 - longueur_bras,
                         largeur_bras, longueur_bras, hauteur, epaisseur_mur,
                         couleur_mur_ext, "Bras bas")
    
    # 4. SOL de toute la structure
    dessiner_sol_croix(ax, centre_x, centre_y, largeur_centrale, longueur_centrale,
                       largeur_bras, longueur_bras, couleur_sol)

def dessiner_rectangle_3d(ax, x, y, largeur, longueur, hauteur, epaisseur_mur, couleur, nom):
    """
    Dessine un rectangle 3D avec des murs d'épaisseur donnée
    """
    # Mur extérieur
    vertices_ext = [
        [x, y, 0], [x + largeur, y, 0], [x + largeur, y + longueur, 0], [x, y + longueur, 0],  # base
        [x, y, hauteur], [x + largeur, y, hauteur], [x + largeur, y + longueur, hauteur], [x, y + longueur, hauteur]  # sommet
    ]
    
    # Mur intérieur (plus petit)
    vertices_int = [
        [x + epaisseur_mur, y + epaisseur_mur, 0], 
        [x + largeur - epaisseur_mur, y + epaisseur_mur, 0], 
        [x + largeur - epaisseur_mur, y + longueur - epaisseur_mur, 0], 
        [x + epaisseur_mur, y + longueur - epaisseur_mur, 0],  # base intérieure
        [x + epaisseur_mur, y + epaisseur_mur, hauteur], 
        [x + largeur - epaisseur_mur, y + epaisseur_mur, hauteur], 
        [x + largeur - epaisseur_mur, y + longueur - epaisseur_mur, hauteur], 
        [x + epaisseur_mur, y + longueur - epaisseur_mur, hauteur]  # sommet intérieur
    ]
    
    # Faces des murs (entre mur extérieur et intérieur)
    faces = []
    
    # Mur avant (y minimum)
    faces.append([vertices_ext[0], vertices_ext[1], vertices_ext[5], vertices_ext[4]])
    faces.append([vertices_int[1], vertices_int[0], vertices_int[4], vertices_int[5]])
    faces.append([vertices_ext[0], vertices_int[0], vertices_int[1], vertices_ext[1]])
    faces.append([vertices_ext[4], vertices_ext[5], vertices_int[5], vertices_int[4]])
    
    # Mur arrière (y maximum)
    faces.append([vertices_ext[2], vertices_ext[3], vertices_ext[7], vertices_ext[6]])
    faces.append([vertices_int[3], vertices_int[2], vertices_int[6], vertices_int[7]])
    faces.append([vertices_ext[2], vertices_ext[3], vertices_int[3], vertices_int[2]])
    faces.append([vertices_ext[6], vertices_int[6], vertices_int[7], vertices_ext[7]])
    
    # Mur gauche (x minimum)
    faces.append([vertices_ext[0], vertices_ext[4], vertices_ext[7], vertices_ext[3]])
    faces.append([vertices_int[0], vertices_int[3], vertices_int[7], vertices_int[4]])
    faces.append([vertices_ext[0], vertices_ext[3], vertices_int[3], vertices_int[0]])
    faces.append([vertices_ext[4], vertices_int[4], vertices_int[7], vertices_ext[7]])
    
    # Mur droit (x maximum)
    faces.append([vertices_ext[1], vertices_ext[2], vertices_ext[6], vertices_ext[5]])
    faces.append([vertices_int[2], vertices_int[1], vertices_int[5], vertices_int[6]])
    faces.append([vertices_ext[1], vertices_int[1], vertices_int[2], vertices_ext[2]])
    faces.append([vertices_ext[5], vertices_ext[6], vertices_int[6], vertices_int[5]])
    
    # Ajouter les faces à l'affichage
    collection = Poly3DCollection(faces, alpha=0.7, facecolor=couleur, edgecolor='black')
    ax.add_collection3d(collection)

def dessiner_sol_croix(ax, centre_x, centre_y, largeur_centrale, longueur_centrale, largeur_bras, longueur_bras, couleur):
    """
    Dessine le sol de la structure en forme de croix
    """
    # Sol de la partie centrale
    sol_central = [
        [centre_x - largeur_centrale/2, centre_y - longueur_centrale/2, 0],
        [centre_x + largeur_centrale/2, centre_y - longueur_centrale/2, 0],
        [centre_x + largeur_centrale/2, centre_y + longueur_centrale/2, 0],
        [centre_x - largeur_centrale/2, centre_y + longueur_centrale/2, 0]
    ]
    
    # Sols des bras
    sols = [sol_central]
    
    # Bras gauche
    sols.append([
        [centre_x - largeur_centrale/2 - longueur_bras, centre_y - largeur_bras/2, 0],
        [centre_x - largeur_centrale/2, centre_y - largeur_bras/2, 0],
        [centre_x - largeur_centrale/2, centre_y + largeur_bras/2, 0],
        [centre_x - largeur_centrale/2 - longueur_bras, centre_y + largeur_bras/2, 0]
    ])
    
    # Bras droit
    sols.append([
        [centre_x + largeur_centrale/2, centre_y - largeur_bras/2, 0],
        [centre_x + largeur_centrale/2 + longueur_bras, centre_y - largeur_bras/2, 0],
        [centre_x + largeur_centrale/2 + longueur_bras, centre_y + largeur_bras/2, 0],
        [centre_x + largeur_centrale/2, centre_y + largeur_bras/2, 0]
    ])
    
    # Bras haut
    sols.append([
        [centre_x - largeur_bras/2, centre_y + longueur_centrale/2, 0],
        [centre_x + largeur_bras/2, centre_y + longueur_centrale/2, 0],
        [centre_x + largeur_bras/2, centre_y + longueur_centrale/2 + longueur_bras, 0],
        [centre_x - largeur_bras/2, centre_y + longueur_centrale/2 + longueur_bras, 0]
    ])
    
    # Bras bas
    sols.append([
        [centre_x - largeur_bras/2, centre_y - longueur_centrale/2 - longueur_bras, 0],
        [centre_x + largeur_bras/2, centre_y - longueur_centrale/2 - longueur_bras, 0],
        [centre_x + largeur_bras/2, centre_y - longueur_centrale/2, 0],
        [centre_x - largeur_bras/2, centre_y - longueur_centrale/2, 0]
    ])
    
    # Dessiner tous les sols
    collection = Poly3DCollection(sols, alpha=0.5, facecolor=couleur, edgecolor='darkgray')
    ax.add_collection3d(collection)

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