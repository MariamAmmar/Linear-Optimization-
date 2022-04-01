#!/usr/bin/env python
# coding: utf-8

# # Linear Optimization Homework 12 
# 

# Question 15.2
# 
# In the videos, we saw the “diet problem”. (The diet problem is one of the first large-scale optimizationproblems to be studied in practice. Back in the 1930’s and 40’s, the Army wanted to meet the nutritionalrequirements of its soldiers while minimizing the cost.) In this homework you get to solve a diet problem with real data. The data is given in the file diet.xls. 
# 
# 1.	Formulate an optimization model (a linear program) to find the cheapest diet that satisfies the maximum and minimum daily nutrition constraints, and solve it using PuLP.  Turn in your code and the solution. (The optimal solution should be a diet of air-popped popcorn, poached eggs, oranges, raw iceberg lettuce, raw celery, and frozen broccoli. UGH!)
# 2.	Please add to your model the following constraints (which might require adding more variables) and solve the new model:
# a.	If a food is selected, then a minimum of 1/10 serving must be chosen. (Hint: now you will need two variables for each food i: whether it is chosen, and how much is part of the diet. You’ll also need to write a constraint to link them.)
# b.	Many people dislike celery and frozen broccoli. So at most one, but not both, can be selected.
# c.	To get day-to-day variety in protein, at least 3 kinds of meat/poultry/fish/eggs must be selected. [If something is ambiguous (e.g., should bean-and-bacon soup be considered meat?), just call it whatever you think is appropriate – I want you to learn how to write this type of constraint, but I don’t really care whether we agree on how to classify foods!]
# ![image.png](attachment:e896d997-795a-4c3a-9931-cb68de3f2119.png)![image.png](attachment:c762d2b8-db49-428c-bd0b-a3b2a208cde8.png)![image.png](attachment:5bd0d6ac-436a-4208-9016-7f63139fadd6.png)![image.png](attachment:249817f2-e00c-4597-b5bb-1a53e16c1e4d.png)

# In[1]:


#Reference: 
#https://www.kdnuggets.com/2019/05/linear-programming-discrete-optimization-python-pulp.html

#Minimize cost
#General Constraints -> Max/Min Nutrition Constraints
    #Constraints = Min of 1/10 serving for each food selected
    #Constraints = Only celery or frozen broccoli, but not both together
    #Constraints = At least 3 kinds of meet/eggs for day-to-day variety

#Variables = 1. Food (choosen or no), 2.How much is part of diet
get_ipython().system('pip install texlive-xetex texlive-fonts-recommended texlive-plain-generic')
get_ipython().system('pip install pulp            # PuLP')
from pulp import *
import pandas as pd

df = pd.read_excel (r'/Users/mariamammar/Downloads/hw12 (11)-SP22/data 15.2/diet.xls',header = 0)

#Fill in na values because I get an error if I don't
df = df.fillna(0)

#Select the rows that represent food values
foods_table = df[0:64]

nutrients = list(foods_table.columns.values)

#Minimum daily intake of calories/nutriets
min_val = df[65:66].values.tolist() 

#Maximum daily intake of calories/nutriets
max_val = df[66:67].values.tolist()


# In[2]:


min_val, max_val


# Here we can see that the soldiers needed at least 1500 calories and at most 2500. 

# In[3]:


food_items = list(foods_table['Foods'])

cost = dict([((i[0]), float(i[1])) for i in foods_table.values.tolist()])

#Set up problem
prob = LpProblem('PuLPTutorial', LpMinimize)

#Structure Nutrients Info
nutrient_values = []
for i in range(0,11):
    nutrient_values.append(dict([(j[0],float(j[i+3])) for j in foods_table.values.tolist()]))

#Define Variables
food_variables = LpVariable.dicts("Foods",food_items,0)
food_variables_selected = LpVariable.dicts("Foods_Selected",food_items,0,1,LpBinary)

#Define Objective Function
prob += lpSum([cost[i]*food_variables[i] for i in food_items]), 'Cost'


# #### Define Constraints

# In[4]:


#First, each food combination must fall within the mix/max calorie and nutrient intake. 
for i in range(0,11):
    prob+=lpSum([nutrient_values[i][j]*food_variables[j] for j in food_items])>= min_val[0][i+3]
    prob+=lpSum([nutrient_values[i][j]*food_variables[j] for j in food_items])>= max_val[0][i+3]
    
#Next, can either have frozen broccoli or raw celery
    prob+=food_variables_selected['Frozen Broccoli'] + food_variables['Celery, Raw'] <= 1
    
#Third, food items included must contain at least 1/10 serving
for f in food_items:
    prob+=food_variables_selected[f] >= food_variables[f] * (0.0000001)

#Also, at least 3 kinds of protein sources. 
    prob += food_variables_selected['Roasted Chicken'] + food_variables_selected['Poached Eggs'] +       food_variables_selected['Scrambled Eggs'] + food_variables_selected['Frankfurter, Beef'] +       food_variables_selected['Kielbasa,Prk'] + food_variables_selected['Hamburger W/Toppings'] +       food_variables_selected['Hotdog, Plain'] + food_variables_selected['Pork'] +       food_variables_selected['Bologna,Turkey'] + food_variables_selected['Ham,Sliced,Extralean'] +       food_variables_selected['White Tuna in Water'] + food_variables_selected['Hotdog, Plain'] +       food_variables_selected['Sardines in Oil'] + food_variables_selected['Chicknoodl Soup'] +       food_variables_selected['Vegetbeef Soup'] + food_variables_selected['Pizza W/Pepperoni']      >= 3


# In[5]:


prob.solve()


# print the foods of the optimal diet
print('Optimization Solution:')
for var in prob.variables():
    if var.varValue > 0:
        if str(var).find('Foods_Selected'):
            print(str(var.varValue) + " units of " + str(var))
            
# print the costs of the optimal diet             
print("Total cost of food = $%.2f" % value(prob.objective))


# This does not give the answer mentioned in the problem maybe because I did not include all of the meat options and because of the constraint that there must be either frozen broccoli OR raw celery. Also, it makes sense since one can imagine that the choice of eggs for a protien source would be more cost effective that a meat source. 
