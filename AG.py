import random
import time
import numpy as np
class ukp:
    capacity=0
    p = []  # Profits Array
    w = []  # Weights Array
    rep = [] # binary [C/Wi]

    def __init__(self, capacity, p, w):
        self.capacity = capacity
        self.p = list(p)
        self.w = list(w)

class population:
    chromosome=[]
    benefit=[]

    def __init__(self, chromosome,benefit):
        self.chromosome=chromosome
        self.benefit=benefit


def one_point_cross_over(father, mother, Pc):
    rand_Pc=random.uniform(0,1)
    if (rand_Pc<Pc):
        i = random.randrange(0, len(father))
        child1 = father[0:i]
        child1 += mother[i:len(father)]

        child2 = mother[0:i]
        child2 += father[i:len(father)]

        return child1, child2
    else: return father,mother

def uniform_cross_over(father,mother,Pc):
    rand_Pc=random.uniform(0,1)
    if (rand_Pc<Pc):
        child1 = ""
        child2 = ""

        for i in range(len(father)):
            if random.randint(0, 1) == 1:
                child1 += mother[i]
                child2 += father[i]
            else:
                child1 += father[i]
                child2 += mother[i]

        return child1, child2
    else: return father,mother




def fitness_function(chromosome, instance): #Calculer le benefit d'un chromosome
    benefit_chromosome = 0
    t1 = 0
    t2 = 0
    for j in range(len(instance.rep)):
        t2 += instance.rep[j]
        dec = int(chromosome[t1:t2], 2)
        benefit_chromosome += dec * instance.p[j]
        t1 = t2
    return benefit_chromosome


def weight_function (chromosome, instance):   #calculer le poid d'un chromosome
    weight=0
    t1=0
    t2=0
    for j in range (len(instance.rep)):
        t2+=instance.rep[j]
        dec=int(chromosome[t1:t2],2)
        weight+=dec*instance.w[j]
        t1=t2
    return weight

def update_population(generation,nb_chromosome):   # Garder les meilleures individus de la population
    new_chromosome=[]
    new_benefit=[]

    index = sorted(range(len(generation.benefit)), key = lambda sub: generation.benefit[sub])[-nb_chromosome:]
    # indices des chromosomes qui ont le meilleure benefit
    for i in range (nb_chromosome):
        new_chromosome.append(generation.chromosome[index[i]])
        new_benefit.append(generation.benefit[index[i]])
    generation=population(new_chromosome,new_benefit)
    return generation


def roulette_wheel (populationS, nb_chromosome,instance):  # Roulette wheel pour la selection

    sum_fitness=0
    relative_fitness=[]
    for i in range (nb_chromosome):
        sum_fitness+=fitness_function(populationS.chromosome[i],instance)
    for i in range (nb_chromosome):
        relative_fitness.append(fitness_function(populationS.chromosome[i],instance)/sum_fitness)


    pick=random.uniform(0,1)
    current=0
    for i in range (nb_chromosome):
        current+=relative_fitness[i]
        if current>pick:
            return i

    



def mutate(child, Pm):
    rand_Pm=random.uniform(0,1)
    ch = list(child)
    if rand_Pm<Pm:
        k = random.randrange(0, len(child))
        ch[k] = 1 - int(ch[k])  # 0 =>1 et 1=>0

    return ''.join(map(str,ch))


def resultat(generation,instance):  #Afficher le meilleure chromosome de la derniére generation
    t1=0
    t2=0
    list=[]

    index = sorted(range(len(generation.benefit)), key = lambda sub: generation.benefit[sub])[-1:]
    chromosome= generation.chromosome[index[0]]

    for j in range (len(instance.rep)):
        t2+=instance.rep[j]
        dec=int(chromosome[t1:t2],2)
        list.append(dec)
        t1=t2

    print("Gain :"+str(generation.benefit[index[0]]))
    print("Poids: "+str(weight_function(generation.chromosome[index[0]],instance)))
    print(list) 




def repair(chromosome,instance,l):
    R=weight_function(chromosome,instance)
    ch=list(chromosome)
    #Drop phase
    for i in range (0,l):   #0: l-1

        if (R>instance.capacity) and (int(ch[i])==1) :
             ch[i]=str(0)
             R=weight_function(''.join(ch),instance)
        if R<=instance.capacity:
            break

    #Add phase
    for i in range (l-1,-1,-1):  # l-1: 0   
       
        if   (R<instance.capacity) and (int(ch[i])==0):
            ch[i]=str(1)
            R=weight_function(''.join(ch),instance)
            if (R>instance.capacity):       # Assurer qu'on dépasse pas la capacité
                ch[i]=str(0)
                R= R=weight_function(''.join(ch),instance)


    return ''.join(ch)







def main():
    # instance= ukp(17,[10,40,50,70], [1,3,4,5])         #capacité, [profit], [weight]
    # instance=ukp(130,[4,5,6,2], [33,49,60,32])
    # nb_items=4

    # OPTION 1
    nb_chromosome = random.randint(50, 80);  # Génerer aléatoiremt
    nb_generation = random.randint(5, 10);  # Générer aléatoirement

    # OPTION 2
    nb_chromosome=int (input("Taille de la population : "))
    nb_generation=int (input("Nombre de generation : "))
    prob_croisement= float(input ("Probabilité de croisement : ")) # 0.9
    prob_mutation = float (input("Probabilité de mutation : "))  # 0.05
    l = 0  # taille chromosome
                                                  
    #Lecture de l'instnace du générateur
    instance_list=[]
    profit_list=[]  
    weight_list=[]  
    
    with open('dt.txt','r') as file:
            for line in file:
                for word in line.split():
                    instance_list.append(word)

    nb_items=int(instance_list[0] )
    capacite=int(instance_list[1] )
    i=2
    print("nombre d'objets :"+str(nb_items))
    print("Capacité du sac :"+str(capacite))
    
    while i<= len(instance_list)-2:
        weight_list.append(int(instance_list[i]))
        profit_list.append(int(instance_list[i+1]))
        i+=2
    instance=ukp(capacite,profit_list,weight_list)

    



    for i in range (0,nb_items):  #Détreminer l taille du chromosome
        instance.rep.append(len(bin(instance.capacity//instance.w[i]).replace("0b","")))
        l=l+instance.rep[i]



    population_init=population([],[])
    for k in range (nb_chromosome): # Créer la population initiale

        chromosome=''.join(map(str,np.random.choice([0, 1], size=(l),p=[0.999,0.001])))

        #transformer les sol non réalisables en sol réalisables
        if weight_function(chromosome,instance)>instance.capacity:
               chromosome=repair(chromosome,instance,l)

        population_init.chromosome.append(chromosome)

    #calculer le benefit de chq chromosome
    for  k in range (nb_chromosome):
        benefit_chromosome=fitness_function(population_init.chromosome[k],instance)
        #print(benefit_chromosome)
        population_init.benefit.append(benefit_chromosome)

    print("-----------------------------------------------------------------------")
    generation=population (population_init.chromosome,population_init.benefit)     #initilaiser generation

    for k in range (nb_generation):
        for i in range (nb_chromosome//2):

            # Selection
              #first chromosme
            index1=roulette_wheel(generation, nb_chromosome,instance)  #index du chromosome selectioné
            n1 = generation.chromosome[index1] # chromosome selectionné
              #Second chromosome
            index2=roulette_wheel(generation,nb_chromosome, instance)
            n2 = generation.chromosome[index2]

            # Croisement  2 OPTIONS
            #n3,n4=one_point_cross_over(n1,n2)
            n3, n4 = uniform_cross_over(n1,n2, prob_croisement)

            # Mutation
            n3 = mutate(n3, prob_mutation)
            if weight_function(n3,instance)>instance.capacity:
                n3=repair(n3,instance,l)

            n4 = mutate(n4, prob_mutation)
            if weight_function(n4,instance)>instance.capacity:
                n4=repair(n4,instance,l)

            # Ajouter les chromosomes enfants à la population
            generation.chromosome.append(n3)
            generation.benefit.append(fitness_function(n3,instance))
            generation.chromosome.append(n4)
            generation.benefit.append(fitness_function(n4,instance))

        #Mettre à jour la population
        generation= update_population(generation,nb_chromosome)

    #Afficher le résultat final

    print("Resultat Final :  ")
    resultat(generation,instance)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
