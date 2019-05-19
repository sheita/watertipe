"""
TIPE
"""

def sep():
    print('\n')

Ions = ['Na+','Cl-','Fe3+', 'HO-']
Concentrations = [3.0e-7, 4.0e-7, 5.0e-2, 0]
Volume = 1 # Volume de la solution en litres 
pH = 7

# Affichage des ions et concentrations
def afficherSolution():
    # Volume
    print('Volume :', Volume, 'L')
    # Ions
    if len(Ions)==len(Concentrations):
        print("Ions présents en solution :")    
        for i in range(len(Ions)):
            print(str(i) + '.', Ions[i], ':', Concentrations[i], 'mol/L')
    else:
        print('Erreur : les listes sont de tailles différentes')
    sep()

def arrondi(x):
    """
    La fonction prend en entrée un flottant x et renvoie son arrondi à 2 chiffres après la virgule.
    Au delà de 0.01 et 1000, l'écriture est scientifique, avec 3 chiffres significatifs
    """
    if not (x >= 0.01 and x <= 1000):
        x = "%.2e"%x
    else:
        x = float(int(x*100))/100
    print(x)

def verification():
    # Concentration en Fe3+
    ConditionFe3 = 1e-10 # Quantité max de Fe3+
    if Concentrations[2]>ConditionFe3:
        print('[Fe3+] trop élevée (>1e-10)')
        hydroxydeFer(ConditionFe3)
    else:
        print('La concentration en Fe3+ est normale')

def hydroxydeFer(ConditionFe3):
    # Fe3+ + 3HO- = Fe(OH)3
    CsoudeLabo = 5.0 # Soude au labo
    # On prend une forte concentration de soude pour dégliger la dilution
    K = 1e38 # Constante 1/Ks; Ks = 1e-38

    # Simplification des concentrations
    CiNa = Concentrations[0]
    CiHO = Concentrations[3]
    CiFe3 = Concentrations[2]
    
    # Affichage des concentrations initiales
    print('[Fe3+]i =', CiFe3)
    print('[Na+]i =', CiNa)
    sep()
    
    # Réaction
    CeqFe3 = ConditionFe3
    xeq = CiFe3 - CeqFe3
    print('xeq =', xeq)
    
    # D'après Guldberg & Waage
    CsoudeNecessaire = (1/(K*CeqFe3))**(1/3) + 3*xeq
    
    # Détermination du volume de Soude à ajouter
    VHOaAjouter = (CsoudeNecessaire*Volume)/CsoudeLabo
    print('On ajoute', VHOaAjouter ,'L de soude à', CsoudeLabo, 'mol/L')
    print('On filtre ensuite le Fe(OH)3 formé')
    
    # La soude contient aussi des ions Na+
    CeqNa = (CiNa*VHOaAjouter)/Volume
    
    # Affichage des concentrations après réaction
    sep()
    print('[Na+]f =', CeqNa)
    print('[Fe3+]f =', CeqFe3)
    
    # Réassignation des concentrations simplifiées
    Concentrations[0] = CeqNa
    Concentrations[1] = CiHO
    Concentrations[2] = CeqFe3


afficherSolution()
