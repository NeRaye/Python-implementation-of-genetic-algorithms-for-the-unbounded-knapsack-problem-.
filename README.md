Python implementation of genetic algorithms (AG) used to solve the unbounded knapsack problem (UKP).


        1. Principe des algorithmes génétiques
Le développement de l'algorithme génétique (GA) est inspiré par la survie du principe le plus apte dans la théorie darwinienne de l'évolution naturelle et la théorie de la génétique de Mendel. La recherche GA commence par un ensemble de solutions, souvent étiquetées comme une population. Chaque solution est représentée comme un chromosome dans la
population. Dans chaque génération, les opérateurs de reproduction tels que la mutation et le croisement sont utilisés pour la création des nouveaux chromosomes. La performance ou l'adéquation d'un chromosome est alors définie par une certaine valeur d'adaptation. Cette valeur d'adaptation d'un chromosome sert de base à sa survie dans la prochaine génération, c'est-à-dire que le chromosome plus en forme a plus de chances de survivre. Ce mécanisme de sélection basé sur la forme physique garantit que les chromosomes les plus aptes survivent à travers les générations, tandis que les moins en forme ne se reproduisent pas bien. Le processus d'évolution se répète jusqu'à ce que certaines conditions d'arrêt soient satisfaites.


        2. Solution proposée pour résoudre un problème UKP avec un algorithme
        génétique:
        
2.1. Codage binaire des chromosomes et création de la population initiale:

On commence par chercher le nombre maximum d’éléments de l’objet xi, que peut contenir le sac, ie : capacité du sac/ poids de l’objet i.
On procède après à la conversion de ce nombre décimale en binaire.
Le nombre de bits nécessaire pour coder l’ensemble des objets, représente la taille du chromosome, on va la noter l.
Pour construire un chromosome on génère aléatoirement un nombre binaire de taille l, en vérifiant la contrainte du poids, pour ne pas dépasser la taille du sac à dos, toute solution impossible est transformée en solution réalisable par la fonction de réparation.

Exemple :
(Gain, Poids) = { (12, 25), (6, 2), (4, 5), (3, 7) }
Sous la contrainte 25 X1+2 X2+5 X3+ 7 X4 <= 36
25 X1<= 36 X1 =1 : sur 1 bits
2 X2<= 36 X2 =18 : sur 5 bits
5 X3<= 36 X3 = 7 : sur 3 bits
7 X4<= 36 X4= 5 : sur 3 bits
La longeur du chromosome est donc égale à 12.

On peut donc avoir un chromosome codé comme suit : 000 00101 011 000, ce qui siginie qu’on a pris 5 unité de X2 et 3 unité de type X3 et X4.
Ainsi on genere aléatoirement N chromosome, pour former la population initiale qui représente la premiére gènèration.

2.1.1. Méchanisme de selection par roue de loterie
La fonction d’adaptation F(n) est définie par : Somme(vi*xi) sur n 
Algorithme de sélection :
        1. Allouer un tableau A de taille N (nombre de chromosomes)
        2. Pour i=1,..., N :
           A[i]=pi = fi/ Somme(fi) sur N
        Ou ‘fi’ est la valeur de la fonction d’adaptation du chromosome i, ‘pi’ est sa probabilité de sélection.
        3. Générer une valeur aléatoire x entre (0,1)
        4. Retourner l’index du plus petit élément cumulé de A plus grand que x.
        
2.1.2. Méchanisme de croisemet
Le croisment est appliqué avec une proba Pc, et nous permet de créer de nouveaux chromosomes. On a implémenté 2 types de croisement :

- Le croisement à un point :
On va généré un nombre aléatoire entre 1 et l, puis sur ce point on va échnger entre les bits des 2 parents pour obtenir 2 nouveaux chromosomes comme suit :
000 0010 | 1 011 000 *001 0010| 1 010 000 = 000 0010 1 010 000 (Enfant1) et 001
0010 1 011 000 (Enfant 2)

- Le croisement uniforme : Generer un masque de taille l, les bits dont l’indice correspondant du masque est égale à 1 sont interchagés.
Masque : 001 00101 001 010
Parent 1 : 100 01101 011 000
Parent 2 : 001 00001 010 000
Enfant 1: 101 01001 010 000
Enfant 2 : 000 00101 011 000

2.1.3. Méchanisme de mutation
Après le croisment vient la mutation, qui est une opération qu’on applique avec une probabilité Pm et qui nous évite de tomber sur des optimums locaux. Elle consite à choisir un bit et le changé de 1 à 0 ou de 0 à 1.

2.1.4. Fonction de réparation
Lors l’application des opérations de croisement et de mutation, les solutions peuvents ne plus respecter la contrainte et dépassent le poids maximal du sac à dos. Ce qui nous amène à implementer cette fonction qui va nous permettre de transformer ces solutions en solutions réalisables.

Algoritme de réparation :
        1. R= F(n) // valeur de la fonction d’adaptation pour le chromosome n
        2. Pour i=1,l :
        Si n[i]=1 et R>V alors n[i] =0
        3. Pour i=l,1 :
        Si n[i]=0 et R<V alors n[i] =1
        V : capacité du sac, l : taille du chromosome
        
Exemple :
Considerons un probléme UKP avec 5 objets, dont la contrainte est la suivante :
R = 77x1 + 65x2 + 88 x3 +52x4 + 90x5 ≤ 1197.

Supposons à une étape on a chromosome = 1110001100010101010100, on aura donc R= 3096 qui est bien supérieure à 1197.

Drop phase : remplacer de gauche à droite les 1 par des 0 tant que la solution n’est pas
réalisable, on aura chromosome= 0000000000000001010100.

Add phase : remplacer de droite à gauche les 0 par des 1 tant que la solution est réalisable,
chromosome= 0000000000001111111111 qui est une solution réalisable.

        1. Mécanisme de remplacement :
        Après avoir introduit les nouveaux chromosomes dans la populations, on doit la mettre à jour,
        la nouvelle génération est alors constituée des meilleurs individus de la population.

        2. Condition d’arrêt :
        Lorsque le nombre maximum de générations est atteint on arrête le déroulement. Et on
        retourne le meilleur individu de la dernière génération comme solution final.

2.2. Pseudo algorithme
Algorithme Algorithme_genetique (k, nb_iterations)
  1. Population = ensemble {n1,n2,.......nk}, généré aléatoirement de k chromosomes
  2. Pour t=1,..., nb iterations
    2.1 pour i=1....k
      2.1.1 n= chromosome pris dans la population avec probabilté qui augmente
      selon F(n)
      2.1.2 n’=chromosome pris dans la populatione de la méme façon
      2.1.3 n*=resultat du crioisement entre n et n’, appliqué avec une proba Pc
      2.1.4 avec petite proba Pm, appliquer une mutation sur n*
      2.1.5 ajouter n* la population
    2.2 Mettre à jours la population , on garndant les k meilleure chromosome
  3. retourner n dans population avec valeur de F(n) la plus élévé
