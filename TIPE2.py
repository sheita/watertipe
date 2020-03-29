# TIPE : Dépollution d'une eau usée

"""
Configuration
"""
# Choix d'une solution pré-enregistrée (1,2,... ou 0 si aucun choix)
solution=2
# Arrondir l'affichage des résultats (True ou False)
arrondir=True

"""
[Base de données]

- Concentrations acceptables de chaque ion en solution au-delà desquelles l'ion devra être traité.
Ici on a choisi les normes de l'OMS qui correspondent à une eau potable, mais le chimiste pourra choisir ses propres valeurs.

- Concentrations des solutions disponibles au laboratoire qui sont nécessaires aux réactions de dépollution programmés

Toutes les concentrations sont en mol/L, les volumes en L, et les quantités de matière en mol.
"""
Normes = {
    "Na+": 0.5,
    "Fe3+": 0.3,
    "Cl-": 1e10,
    "HO-": 1e10 # arbitrairement grand
}

Labo = {
    "Soude": 5.0
}

# DEBUT DU PROGRAMME

print("Assistant de dépollution d'eau usée")

"""
[Fonctions auxiliaires]

- sep() permet d'afficher un séparateur dans la console pour améliorer la lisibilité

- rechercheIndice(sym) retourne l'indice dans la liste Ions qui correspond au symbole de l'ion donné en argument
ex: rechercheIndice("Fe3+") renvoie 2

- arrondi(x) prend en entrée un flottant x et renvoie son arrondi à 2 chiffres après la virgule (au delà de 0.01 et 1000, l'écriture est scientifique, avec 3 chiffres significatifs)
"""

def sep():
    print("------------------------")
sep()

def rechercheIndice(sym):
    for i in range(len(Ions)):
        if Ions[i][0]==sym:
            return i
    return None

def arrondi(x):
    if arrondir:
        if not (x >= 0.01 and x <= 1000):
            x = "%.2e"%x
        else:
            x = float(int(x*100))/100
        return x
    else:
        return x

"""
[Données en entrée]

La liste Ions va contenir les informations concernant les ions présents dans la solution (symbole, concentration, ...) dans des sous-listes.

Ions[i][d] permettera d'accéder à la composante d de l'ion d'indice i

Composantes : 0 pour le symbole, 1 pour la concentration, 2 pour l'état de traitement

ex:
Ions[0][0] renvoie le symbole de l'ion d'indice 0
Ions[3][1] renvoie la concentration de l'ion d'indice 3
Ions[rechercheIndice('Na+')][1] renvoie la concentration de l'ion Na+
"""
Ions = []
Volume = 0 # en L

# Cas des solutions pré-enregistrées
if solution==1:
    Ions = [['Na+', 3.0e-7],
        ['Cl-', 0.3],
        ['Fe3+', 0.8],
        ['HO-', 0],
        ['Gp2+', 6e-2]]
    Volume = 0.02
elif solution==2:
    Ions = [['Cl-', 0.4],
        ['Fe3+', 0.8],
        ['SO42-', 1.0]]
    Volume = 0.02

# Pas de choix de solution pré-enregistrée : le programme demande le volume, les ions et leurs concentrations
else:
    Volume = float(input("Quel est le volume de la solution en L ?"))
    n = int(input("Combien d'ions sont présents en solution ?\n"))
    for i in range(n):
        L = []
        L.append(input("Symbole de l'ion n°%s: "%str(i+1)))
        L.append(float(input("[%s] = "%L[0])))
        Ions.append(L)
        sep()

"""
[Charge globale]

Cette fonction calcule la charge globale de la solution en identifiant la contribution de chaque ion grace à son symbole et à sa concentration.

Elle renvoie la charge globale de celle-ci qui pourra plus tard être comparée pour vérifier sa neutralité.
"""

def chargeGlobale():
    sep()
    chargeGlobale = 0
    print("Vérification de la neutralité:")
    for x in Ions:
        signe, nombre = 0, 0
        if x[0][-1] == "+":
            signe = 1
        elif x[0][-1] == "-":
            signe = -1
        else:
            print("Erreur charge pour", x[0])
        
        if x[0][-2] in "23456789":
            nombre = x[0][-2]
        else:
            nombre = 1
        
        chargeGlobale = chargeGlobale + float(signe)*float(nombre)*x[1]
        chargeGlobale = round(chargeGlobale, 3)
        print("%s (%s%s)"%(x[0],x[0][-1],nombre))
    
    return chargeGlobale

"""
[Etat de la solution]

Cette fonction affiche le volume total actuel de la solution, la liste des ions dans cette solution et affiche si la solution est neutre.
"""

def etatSolution():
    sep()
    print("La solution contient %s ions dans %sL:"%(len(Ions),arrondi(Volume)))
    for i in range(len(Ions)):
        print("%s: [%s] = %s mol/L"%(i,Ions[i][0],arrondi(Ions[i][1])))
    
    charge = chargeGlobale()
    if charge == 0.:
        print("La solution est neutre")
    else:
        print("La solution n'est pas neutre\nSa charge globale est de %s"%charge)
    sep()

"""
[Analyse]

Cette fonction analyse la solution à l'aide du dictionnaire Normes qui contient les concentrations acceptables de chaque ion en solution.

Etats de traitement possibles : AT (à traiter), T (déjà traité ou traitement non nécessaire), NA (non reconnu par le programme)
"""
dejaAnalyse = False

def analyse():
    sep()
    
    global dejaAnalyse
    if dejaAnalyse:
        for i in range(len(Ions)):
            Ions[i] = Ions[i][:2]
    
    print("Résultats de l'analyse :")
    for x in Ions:
        if x[0] in Normes:
            if x[1]>Normes[x[0]]:
                x.append('AT')
                print("✴️ %s à traiter"%x[0])
            else:
                x.append('T')
                print("✅ %s OK"%x[0])
        else:
            x.append('NA')
            print("⚠️ %s n'est pas reconnu"%x[0])
    
    dejaAnalyse = True
    sep()

"""
[Les fonctions de traitement]

Chaque fonction de traitement réalise des calculs pour traiter les ions indépendamment les uns des autres. Chacune des fonctions a un état initial et un état final et il faut prendre en compte l'évolution de TOUS les ions.
"""

def traitementFe3():
    """
    Réaction de précipitation :
    Fe3+ + 3HO- = Fe(OH)3
    Constante de vitesse :
    K = 1e38
    """
    sep()
    iFe3 = rechercheIndice("Fe3+")
    print("L'indice de Fe3+ est %s"%iFe3)
    CfFe3 = Normes["Fe3+"]
    print("On veut que [Fe3+] = %s mol/L"%CfFe3)
    xeq = Ions[iFe3][1] - CfFe3
    print("On fixe xeq = %s"%xeq)
    CiSoude = (1/(1e38*CfFe3))**(1/3) + 3*xeq
    global Volume
    ViSoude = (CiSoude/(Labo["Soude"]-CiSoude))*Volume
    print("Le volume de soude à ajouter sera de %sL à la concentration %s mol/L"%(arrondi(ViSoude),Labo["Soude"]))
    
    Vfinal = Volume + ViSoude
    print("Le volume de la solution passe de  %sL à %sL"%(arrondi(Volume),arrondi(Vfinal)))
    
    # Mise à jour des concentrations
    Ions[iFe3][1]=CfFe3
    
    CfNa = CiSoude
    iNa = rechercheIndice("Na+")
    if iNa != None:
        Ions[iNa][1] = CfNa*(ViSoude/Vfinal)
        print("[Na+] = %s mol/L a été mise à jour"%arrondi(CfNa))
    else:
        Ions.append(["Na+",CfNa,"T"])
        print("[Na+] = %s mol/L ajouté à la liste des ions en solution"%arrondi(CfNa))
        
    for x in Ions:
        if x[0] not in ('Fe3+', 'HO-', 'Na+'):
            x[1]*=Volume/Vfinal
    sep()
    
    Volume = Vfinal
    
    RtFe3 = [ViSoude, Labo["Soude"]]
    Ions[iFe3].append(RtFe3)
    
    Ions[iFe3][2] = "T"

"""
[Affichage des protocoles]

La fonction affiche les protocoles à réaliser par le chimiste pour dépolluer son eau.

Les protocoles sont disponibles dans des fichiers au format .txt placés dans le même dossier que ce programme. La fonction y ajoute les valeurs calculées à l'issue des traitements aux bons emplacements.
"""
def afficherProtocoles():
    sep()
    protocoleFe3 = open("protocolePrecipitationFe3.txt","r",encoding="utf-8")
    
    for x in protocoleFe3:
        print(x.replace("#1",str(arrondi(Ions[rechercheIndice("Fe3+")][3][0]))).replace("#2",str(arrondi(Ions[rechercheIndice("Fe3+")][3][1]))), end="")
        
    protocoleFe3.close()
    sep()
