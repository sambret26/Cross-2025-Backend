# DISCORD
TOTAL_REWARDS = "Le nombre de récompensés total est paramétré sur TOTAL_REWARDS.\nPour le mettre à jour, utilisez la commande $totalRewards [nombre]"
FROM_ADRESS = "L'adresse d'envoie actuelle est FROM_ADRESS.\nPour la mettre à jour, envoyer la commande $fromAdress [exemple@mail.com]."
TO_ADRESS = "L'adresse destinataire actuelle est TO_ADRESS.\nPour la mettre à jour, envoyer la commande $toAdress [exemple@mail.com]."
INVALID_OFFSETS = "Les offsets n'ont pas été correctement définis.\nPour les définir, utilisez la commande $offsets [a] [b] [c]"
INVALID_DEBUG = "Le mode debug n'est pas correct.\nPour le définir, utilisez la commande $debug [on|off]"
ALL_REWARDS_KNOWN = "Tous les récompensés sont connus, un mail a été envoyé à l'adresse TO_ADRESS."
TOTAL_REWARDS_SET = "Le nombre de récompensés a été défini sur TOTAL_REWARDS."
ERROR_TOTAL_REWARD = "Erreur lors de la récupération du nombre de récompensés"
OFFSETS_CMD = "\nPour les définir, utilisez la commande $offsets [a] [b] [c]"
UNKNOWN_FORMAT = "Format du fichier non reconnue. Fichier non pris en compte"
SEND_MAIL = "Pour envoyer le mail récapitulatif, utilisez la commande $mail."
FROM_ADRESS_SET = "L'adresse d'envoie a été définie sur FROM_ADRESS."
TO_ADRESS_SET = "L'adresse destinataire a été définie sur TO_ADRESS."
ERROR_FETCHING_OFFSET = "Erreur lors de la récupération des offsets"
FILE_TREATED = "Fichier traité par le PC_NAME en DURATION secondes"
INVALID_REWARDS = "Le nombre de récompensés n'est pas correct."
DEBUG_ERROR = "Erreur lors de la récupération du mode debug"
CHANNEL_ERROR = "Erreur lors de la récupération du channel"
MAIL_SENT = "Le mail a été envoyé à l'adresse TO_ADRESS"
OFFSETS_SET = "Les offsets ont été définis sur A, B, C."
RESULT = "Nombre de coureurs arrivés : ARRIVED/TOTAL\n"
CLASSIC_START = "Programme démarré en mode classique"
REWARD_FILE = "Voici le tableau des récompenses :"
REWARDS_LIST = "Voici la liste des recompensés :"
INVALID_ADRESS = "L'adresse n'est pas correcte."
DB_INIT = "La base de données à été initialisée"
DEBUG_START = "Programme démarré en mode débug"
DEBUG_OFF = "Le mode debug a été desactivé"
OFFSETS = "Offsets : a: A : b: B : c: C"
DEBUG_ON = "Le mode debug a été activé"
OK = "Ok reader"

# ERRORS
ERROR_FETCHING_TO_ADRESS = "Erreur lors de la récupération de l'adresse destinataire"
ERROR_FETCHING_FROM_ADRESS = "Erreur lors de la récupération de l'adresse d'envoie"
ERROR_TOTAL_REWARD = "Erreur lors de la récupération du nombre de récompensés"
ERROR_OFFSET = "Erreur lors de la récupération des offsets"
ERROR_REWARD = "Erreur lors du comptage des récompensés"
ERROR_SENDING_MAIL = "Erreur lors de l'envoie du mail"
COUNT_ERROR = "Erreur lors du comptage des coureurs"

#CMD
CMD = "Voici la liste des commandes disponibles:\n \
    $mail : Envoyer un mail contenant le fichier des récompensés à l'adresse définie\n \
    $init : Initialiser la base de données (Suppression des joueurs et initialisation des paramètres)\n \
    $test : Demande une confirmation à tous les programmes lancés\n \
    $file : Génère et répond le fichier des récompensés\n \
    $fromAdress [exemple@mail.com] : Affiche ou modifie l'adresse d'envoie\n \
    $toAdress [exemple@mail.com] : Affiche ou modifie l'adresse destinataire\n \
    $offsets [a] [b] [c] : Affiche ou modifie les offsets\n \
    $totalRewards [nombre] : Affiche ou modifie le nombre de récompensés\n \
    $debug [on|off] : Affiche ou modifie le mode debug\n \
    $clear [nombre] : Supprime les derniers messages\n \
    $cmd : Affiche la liste des commandes disponibles"