import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des constantes
LARGEUR_FENETRE = 800
HAUTEUR_FENETRE = 600
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
NB_ERREURS_MAX = 7

# Chargement des mots depuis le fichier "mots.txt"
with open("mots.txt", "r") as f:
    mots = [mot.strip().upper() for mot in f.readlines()]

# Fonction pour choisir un mot aléatoire dans la liste de mots
def choisir_mot():
    return random.choice(mots)

# Définition des variables du jeu
lettres_trouvees = set()
lettres_ratees = set()
nb_erreurs = 0
game_over = False

# Chargement des images
images_pendu = [pygame.image.load(f"images/pendu{i}.png") for i in range(NB_ERREURS_MAX + 1)]

# Ouverture de la fenêtre de jeu
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Jeu du pendu")

# Fonction pour afficher le texte
def afficher_texte(texte, font, couleur, x, y):
    surface_texte = font.render(texte, True, couleur)
    fenetre.blit(surface_texte, (x, y))

# Fonction pour afficher le mot à deviner avec des '_'
def afficher_mot(mot):
    mot_affiche = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            mot_affiche += lettre
        else:
            mot_affiche += "_"
    afficher_texte(mot_affiche, pygame.font.SysFont("arial", 50), NOIR, LARGEUR_FENETRE/2 - 25*len(mot)/2, HAUTEUR_FENETRE/2)

# Boucle principale du jeu
while True:
    # Menu principal
    afficher_texte("Menu principal", pygame.font.SysFont("arial", 50), NOIR, LARGEUR_FENETRE/2 - 150, 50)
    afficher_texte("1. Jouer", pygame.font.SysFont("arial", 30), NOIR, 100, 200)
    afficher_texte("2. Insérer un mot", pygame.font.SysFont("arial", 30), NOIR, 100, 250)
    pygame.display.update()

    choix = None
    while choix is None:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evenement.type == pygame.KEYDOWN:
                if evenement.unicode == "1":
                    choix = "JOUER"
                elif evenement.unicode == "2":
                    choix = "INSERER"
    
    # Jeu
    if choix == "JOUER":
        # Choix aléatoire d'un mot à deviner
        mot_secret = choisir_mot()
        lettres_trouvees = set()
        lettres_ratees = set()
                # Boucle de jeu
        while not game_over:
            # Affichage de l'image du pendu correspondant au nombre d'erreurs
            fenetre.blit(images_pendu[nb_erreurs], (LARGEUR_FENETRE/2 - 150, 100))

            # Affichage du mot à deviner
            afficher_mot(mot_secret)

            # Affichage des lettres déjà essayées
            afficher_texte("Lettres déjà essayées :", pygame.font.SysFont("arial", 20), NOIR, 50, 450)
            afficher_texte(", ".join(sorted(lettres_ratees)), pygame.font.SysFont("arial", 20), NOIR, 50, 480)

            # Gestion des événements
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif evenement.type == pygame.KEYDOWN:
                    if evenement.unicode.isalpha():
                        lettre = evenement.unicode.upper()
                        if lettre in lettres_trouvees or lettre in lettres_ratees:
                            continue
                        elif lettre in mot_secret:
                            lettres_trouvees.add(lettre)
                            if len(lettres_trouvees) == len(set(mot_secret)):
                                game_over = True
                        else:
                            lettres_ratees.add(lettre)
                            nb_erreurs += 1
                            if nb_erreurs == NB_ERREURS_MAX:
                                game_over = True

            # Actualisation de la fenêtre de jeu
            pygame.display.update()

        # Affichage du résultat de la partie
        if len(lettres_trouvees) == len(set(mot_secret)):
            afficher_texte("Gagné !", pygame.font.SysFont("arial", 50), VERT, LARGEUR_FENETRE/2 - 100, 400)
        else:
            afficher_texte("Perdu !", pygame.font.SysFont("arial", 50), ROUGE, LARGEUR_FENETRE/2 - 100, 400)
            afficher_texte(f"Le mot était : {mot_secret}", pygame.font.SysFont("arial", 30), NOIR, LARGEUR_FENETRE/2 - 150, 450)

        # Attente d'une action de l'utilisateur pour recommencer ou quitter le jeu
        afficher_texte("Appuyez sur espace pour rejouer ou sur entrée pour quitter", pygame.font.SysFont("arial", 20), NOIR, LARGEUR_FENETRE/2 - 250, 550)
        pygame.display.update()

        recommencer = None
        while recommencer is None:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif evenement.type == pygame.KEYDOWN:
                    if evenement.unicode == " ":
                        recommencer = True
                    elif evenement.key == pygame.K_RETURN:
                        recommencer = False

        if recommencer:
            # Réinitialisation des variables pour une nouvelle partie
            lettres_trouvees = set()
            lettres_ratees = set()
            nb_erreurs = 0
            game_over = False
        else:
            # Sortie de la boucle principale et fermeture de la fenêtre de jeu
            break