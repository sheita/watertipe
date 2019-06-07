# TIPE
# https://github.com/sheita/watertipe

# Comme le script s'exécute en console uniquement, la fonction sep() permet d'ajouter des séparations qui améliorent la lecture
def sep():
    print('\n')

"""
# Données en entrée

Les ions initialement présents en solution sont dans la liste Ions et leurs concentrations respectives sont dans la liste Concentrations.

Exemple: L'ion chlorure correspond à l'indice 1, son symbole est accessible avec Ions[1] et sa concentration avec Concentrations[1].

Le volume initial est nécessaire pour les calculs.
"""

Ions = ['Na+','Cl-','Fe3+', 'HO-']
Concentrations = [3.0e-7, 4.0e-7, 5.0e-2, 0]
Volume = 1 # Volume de la solution en litres 
pH = 7


# Affichage des ions et concentrations
def afficherSolution():
    """
    La fonction afficherSolution() affiche dans la console le volume et l'indice, le symbole et la concentration de la solution à l'état actuel.
    
    La fonction est exécutée automatiquement au lancement du script et affiche donc les données initiales.
    """
    
    # Volume
    print('Volume :', Volume, 'L')
    # Ions : boucle for car on affiche la concentration de chaque ion
    if len(Ions)==len(Concentrations):
        print("Ions présents en solution :")    
        for i in range(len(Ions)):
            print(str(i) + '.', Ions[i], ':', Concentrations[i], 'mol/L')
    else:
        # Si les listes sont de tailles différentes, tous les ions n'ont pas de concentration respective ou vice versa
        print('Erreur : les listes sont de tailles différentes')
    sep()

def arrondi(x):
    """
    La fonction prend en entrée un flottant x et renvoie son arrondi à 2 chiffres après la virgule.
    Au delà de 0.01 et 1000, l'écriture est scientifique, avec 3 chiffres significatifs.
    """
    if not (x >= 0.01 and x <= 1000):
        x = "%.2e"%x
    else:
        x = float(int(x*100))/100
    print(x)

def verification():
    """
    La fonction verification() vérifie un à un les critères qui garantissent qu'une eau est potable et si les conditions ne sont pas respectés, elle exécute les fonctions de chaque réaction chimique utilisée pour y remédier.
    """
    # Concentration en Fe3+
    ConditionFe3 = 1e-10 # Quantité max de Fe3+
    if Concentrations[2]>ConditionFe3:
        print('[Fe3+] trop élevée (>1e-10)')
        hydroxydeFer(ConditionFe3)
        sep()
    else:
        print('La concentration en Fe3+ est normale')

# Si la concentration en ions fer (III) est trop forte par rapport au seuil de potabilité, la fonction hydroxydeFer() est exécutée
def hydroxydeFer(ConditionFe3):
    """
    La fonction hydroxydeFer() effectue les calculs qui permettront d'adapter la concentration en ions Fe3+ grâce à la réaction :
    Fe3+ + 3HO- = Fe(OH)3
    
    Un certain volume de soude (Na+, HO-) doit être ajouté.
    """
    CsoudeLabo = 5.0 # Concentration de soude disponible au labo
    # On prend une forte concentration de soude pour pouvoir dégliger la dilution dans les calculs
    
    # Constante d'équilibre
    K = 1e38 # 1/Ks; Ks = 1e-38

    # Les variables CiX permettent de simplifier la lecture des calculs dans le script, plutot que de manipuler les variables Concentrations[i] directement
    CiNa = Concentrations[0]
    CiHO = Concentrations[3]
    CiFe3 = Concentrations[2]
    
    # Réaction : on souhaite que la concentration des ions Fe3+ à l'équilibre soit égale à la concentration donc on adapte le xeq (avancement à l'équilibre)
    CeqFe3 = ConditionFe3
    xeq = CiFe3 - CeqFe3
    print('xeq =', xeq)
    
    # Ici l'inconnue est le volume de soude qu'il faudra ajouter pour réaliser la réaction
    
    # D'après Guldberg & Waage (calculé à la main)
    CsoudeNecessaire = (1/(K*CeqFe3))**(1/3) + 3*xeq
    
    # Détermination du volume de soude à ajouter
    VsoudeAajouter = (CsoudeNecessaire*Volume)/CsoudeLabo
    
    # Affichage des résultats
    print('On ajoute', VsoudeAajouter ,'L de soude à', CsoudeLabo, 'mol/L')
    print('On filtre ensuite le Fe(OH)3 formé')
    
    # La soude contient aussi des ions Na+
    CeqNa = (CiNa*VsoudeAajouter)/Volume
    
    # Réassignation des concentrations simplifiées
    Concentrations[0] = CeqNa
    Concentrations[1] = CiHO
    Concentrations[2] = CeqFe3

"""
Les fonctions suivantes sont exécutées directement au lancement du script :
"""
afficherSolution()
