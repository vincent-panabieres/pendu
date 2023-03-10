import pygame
import random

pygame.init()

LARGEUR_FENETRE = 800
HAUTEUR_FENETRE = 600
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
NB_ERREURS_MAX = 7
with open("mots.txt", "r") as f:
    mots = [mot.strip().upper() for mot in f.readlines()]

def choisir_mot():
    return random.choice(mots)

lettres_trouvees = set()
lettres_ratees = set()
nb_erreurs = 0
game_over = False

images_pendu = [pygame.image.load(f"images/pendu{i}.png") for i in range(NB_ERREURS_MAX + 1)]

fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Jeu du pendu")

def afficher_texte(texte, font, couleur, x, y):
    surface_texte = font.render(texte, True, couleur)
    fenetre.blit(surface_texte, (x, y))

def afficher_mot(mot):
    mot_affiche = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            mot_affiche += lettre
        else:
            mot_affiche += "_"
    afficher_texte(mot_affiche, pygame.font.SysFont("arial", 50), NOIR, LARGEUR_FENETRE/2 - 25*len(mot)/2, HAUTEUR_FENETRE/2)

while True:
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
    
    if choix == "JOUER":
        mot_secret = choisir_mot()
        lettres_trouvees = set()
        lettres_ratees = set()
                # Boucle de jeu
        while not game_over:
            fenetre.blit(images_pendu[nb_erreurs], (LARGEUR_FENETRE/2 - 150, 100))

            afficher_mot(mot_secret)

            afficher_texte("Lettres déjà essayées :", pygame.font.SysFont("arial", 20), NOIR, 50, 450)
            afficher_texte(", ".join(sorted(lettres_ratees)), pygame.font.SysFont("arial", 20), NOIR, 50, 480)

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

            pygame.display.update()

        if len(lettres_trouvees) == len(set(mot_secret)):
            afficher_texte("Gagné !", pygame.font.SysFont("arial", 50), VERT, LARGEUR_FENETRE/2 - 100, 400)
        else:
            afficher_texte("Perdu !", pygame.font.SysFont("arial", 50), ROUGE, LARGEUR_FENETRE/2 - 100, 400)
            afficher_texte(f"Le mot était : {mot_secret}", pygame.font.SysFont("arial", 30), NOIR, LARGEUR_FENETRE/2 - 150, 450)

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
            lettres_trouvees = set()
            lettres_ratees = set()
            nb_erreurs = 0
            game_over = False
        else:
            break
