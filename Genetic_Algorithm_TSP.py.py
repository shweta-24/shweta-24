#!/usr/bin/env python
# coding: utf-8

# In[19]:


import sys
import math
import random
import operator
import time

cities_dist = {}


# In[21]:


def get_input():
    #print("reached get_input ")
    n = int(input())
    pts = [[0 for i in range(2)] for j in range(n)]
    #cities_dist = {}
    for i in range(n):
        pts[i] = input().split()
        pts[i] = list(map(float, pts[i]))
        
    for i in range(n):
        cities_dist.update({i:[pts[i][0],pts[i][1]]})    
    
    return cities_dist


# In[22]:


def find_distance(c1, c2):
    #print("reached find_distance ")
    return int(math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2))
    


# In[23]:


def find_fitness(tour):
    #print("reached find_fitness ")
    path_distance = 0
    for i in range(len(tour)-1):
        path_distance = path_distance + find_distance([cities_dist[tour[i]][0],cities_dist[tour[i]][1]],[cities_dist[tour[i+1]][0],cities_dist[tour[i+1]][1]])
    return 1/path_distance


# In[24]:


def create_population():
    #print("reached create_population ")
    tour = list(cities_dist.keys())
    init_pop = {0:tour}
    for i in range((len(tour))-1):
        route = random.sample(tour, len(tour))
        init_pop.update({i+1:route})
    return init_pop


# In[25]:


def rank_tours(population):
    #print("reached rank_tours ")
    fitness ={}
    for i in range(len(population)):
        fitness.update({list(population.keys()).index(i):find_fitness(population[i])})
    return sorted(fitness.items(), key=operator.itemgetter(1), reverse=True)


# In[26]:


def mating_pool_selection(ordered_fitness):
    #print("reached mating_pool_selection ")
    selected_pop = []
    cumsum_dict = {}
    j =0
    #print(ordered_fitness)
    for i in range(len(ordered_fitness)):
        cum_sum = 0
        for j in range(i+1):
            cum_sum = cum_sum + list(ordered_fitness)[j][1]
        cumsum_dict.update({i:cum_sum})
    percentile_dict = {}
    for i in range(len(cumsum_dict)):
        percentile_dict.update({i:100*(cumsum_dict[i])/(cumsum_dict[len(cumsum_dict)-1])})
    #print(cumsum_dict)
    #print(percentile_dict)
    while(len(selected_pop)<2):
        selected_pop = []
        for i in range(len(percentile_dict)):
            random_percentile = random.randint(1,100)
            if percentile_dict[i] >=  random_percentile:
                selected_pop.append(i)
    
    return selected_pop


# In[27]:


def select_parents(selected_pop,population):
    #print("reached select_parents ")
    selected_parents = []
    parent_1 = 0
    parent_2 = 0
    while(parent_1 == parent_2):
        parent_1 =  random.randint(0,len(selected_pop)-1)
        parent_2 =  random.randint(0,len(selected_pop)-1)
    selected_parents.append(population[parent_1])
    selected_parents.append(population[parent_2])
    return selected_parents


# In[28]:


def breeding(parent_1, parent_2):
    #print("reached breeding ")
    child = [-1]*len(parent_1)
    gene_1_parent = random.randint(0,len(parent_1)-1)
    gene_2_parent = random.randint(0,len(parent_1)-1)
    start_gene = min(gene_1_parent,gene_2_parent)
    end_gene = max(gene_1_parent,gene_2_parent)
    for i in range (start_gene,end_gene+1):
        child[i]= parent_1[i]
    j = 0
    for i in range(len(child)):
        if child[i] == -1 and parent_2[j] not in child:
            child[i] = parent_2[j]
            j = j+1
        elif child[i] == -1 and parent_2[j] in child:
            while(parent_2[j] in child):
                j = j+1
            child[i] = parent_2[j]
    #print(child)
    
    return child


# In[29]:


def breed_population(mating_pool, population):
    #print("reached breed_population ")
    children = {}
    for i in range(len(mating_pool)):
        parents = select_parents(mating_pool, population)
        child = breeding(parents[0],parents[1])
        children.update({i:child})
    return children
        


# In[30]:


def mutate(tour):
    #print("reached mutate ")
    mutation_rate = 0.05
    for i in range(len(tour)):
        if(random.randint(0,100)<mutation_rate):
            swap_index = random.randint(0,len(tour)-1)
            city1 = tour[i]
            tour[i] = tour[swap_index]
            tour[swap_index] = city1
    return tour


# In[31]:


def mutate_population(population):
    #print("reached mutate_population ")
    mutated_pop = {}
    for i in range(len(list(population.keys()))):
        mutated_pop.update({i:mutate(population[i])})
    return mutated_pop


# In[32]:


def next_generation(current_generation):
    #print("reached next_generation ")
    ordered_population = rank_tours(current_generation)
    #print(ordered_population)
    mating_pool = mating_pool_selection(ordered_population)
    while(len(mating_pool)<2):
        mating_pool = mating_pool_selection(ordered_population)
    #print(mating_pool)
    children = breed_population(mating_pool, current_generation)
    #print(children)
    next_generation = mutate_population(children)
    return next_generation
    
    
    


# In[33]:


def genetic_algorithm(cities_dist):
    #print("reached genetic_algorithm ")
    generation = 10000
    tstart = time.time()
    population = create_population()
    while(generation>=0):
        if time.time()-tstart >= 1.7:
            break
        else:
            #print(time.time()-tstart)
            population = next_generation(population)
            generation = generation-1
            #print(population)
    best_route = population[rank_tours(population)[0][0]]
    best_route_cost = rank_tours(population)[0][1]
    return best_route, best_route_cost
    


# In[34]:


cities_dist = get_input()
best_route, best_route_cost = genetic_algorithm(cities_dist)
for i in best_route:
    print(best_route[i])
#print(best_route)
#print(best_route_cost)


# In[ ]:





# #### 

# In[ ]:





# In[ ]:




