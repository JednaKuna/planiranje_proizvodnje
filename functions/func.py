import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def quantities_table(quantities, time):
    #Napraviti listu mjeseci, moguće generirati prema inputu
    period = [i for i in range(1, time+1)]

    #Napraviti popis količine narudžbi, moguće napumiti inputom
    forecast = quantities

    #Izrada dicitionaria od kojeg ću napraviti DataFrame
    d = {'period': period, 'forecast': forecast}

    #Izrada DataFrame-a
    data = pd.DataFrame(data=d)
    
    return(data)

def first_order(set_up, holding, data_calc):
    
    # Prva narudzba
    # Provjera
    if not isinstance(data_calc, pd.DataFrame):
        print("Input is not a DataFrame!")
        return
    
    order = 1
    
    # Iteriramo kroz svaki redak u tablici
    for index, row in data_calc.iterrows():
        current_month = data_calc.loc[index,'period']
        cost = 0
        
        # Prva priprema
        cost += set_up
        if current_month > 1:
            for t in range(1, current_month+1):
                cost += (t-1) * data_calc.loc[t-1,'forecast'] * holding
        data_calc.loc[index,'Order {}'.format(order)] = cost
    
    return (data_calc)

def other_orders(set_up, holding, data_calc, time_frame):
    
        # Ostale narudzbe
    for order in range(2, time_frame+1):
        for index, row in data_calc.iterrows():
            current_month = data_calc.loc[index,'period']
            if current_month >= order:
                cost = 0

                # Najbolja opcija za prvi period
                values = list(data_calc.loc[order-2,['Order {}'.format(i) for i in range(1, order+1)]].values)
                best = min([i for i in values if i >0])

                # Zbrajanje
                cost += best + set_up
                for t in range(order, current_month+1):
                    cost += (t-order) * data_calc.loc[t-1,'forecast'] * holding
                data_calc.loc[index,'Order {}'.format(order)] = cost
                
    return(data_calc)

def backward(time_frame, data, data_calc):
    
   costs, initials, nexts, quantities = [], [], [], []
   i = time_frame
   while i>0:
       # Order s najmanjim troškovima
       initial_step = i
       next_step = data_calc[data_calc[i]>0][i].idxmin()
       cost = data_calc[data_calc[i]>0][i].min()
       
       # Idući korak
       next_id = int(next_step.replace('Order ',''))
       i = next_id - 1
       
       # Količina
       quantity = data[data['period'].isin(range(next_id, initial_step+1))]['forecast'].sum()
       
       # Popunjavanje lista
       costs.append(cost)
       initials.append(initial_step)
       nexts.append(next_id)
       quantities.append(quantity)
   df_results = pd.DataFrame({'backward':range(1, len(initials)+1),
                           'initial':initials,
                           'nexts':nexts,
                           'cost':costs,
                           'quantity':quantities}).set_index('backward')
   print("Total Cost: {:,}e".format(df_results.cost.sum()))
   
   return(df_results)
   
def calculation(setup_cost, hold_cost, production_cost, df_results, data):
    
    # Rezultat
    results_final = data.copy()

    # Proizvodnja
    month_prod = df_results['nexts'].values
    prod_dict = dict(zip(month_prod, df_results.quantity.values))

    # Values
    results_final['production'] = results_final['period'].apply(lambda t: prod_dict[t] if t in month_prod else 0)

    # Inventory On Hand
    results_final['IOH'] = (results_final['production'] - results_final['forecast']).cumsum()

    # Holding Cost
    results_final['Holding Cost'] = (results_final['IOH'] * hold_cost)

    # Set Up Cost
    results_final['Set-Up Costs'] = results_final['production'].apply(lambda t: setup_cost if t > 0 else 0)

    # Holding + Set-Up
    results_final['Holding + Set-Up'] = results_final[['Holding Cost', 'Set-Up Costs']].sum(axis = 1)

    # Ukupno 
    results_final['Total Cost'] = (results_final['production'] * production_cost) + results_final['Set-Up Costs'] + results_final['Holding Cost']

    return(results_final)


    
def cost_comparison(setup_cost, production_cost, time_frame, results_final):
    
    #Izračum ukupnih troškova tjekom odabranog perioda
    # Standardni troskovi: tu sam racunao samo troskove pripreme (bez troskova skladistenja)
    s = [0] * time_frame
    s[0]= setup_cost

    for i in range(1,time_frame):
        s[i] = (s[i-1] + setup_cost)
        
    ss = [i * production_cost for i in results_final['forecast'].tolist()]
    
    for i in range(1,time_frame):
        ss[i] = (ss[i] + ss[i-1])

    standardni_troskovi = np.add(s,ss).tolist()

    #Optimalni troskovi
    optimalni_troskovi = results_final['Total Cost'].tolist()
    t = [0] * time_frame
    t[0] = optimalni_troskovi[0]

    for i in range(0,time_frame):
        t[i] = t[i-1]+optimalni_troskovi[i]
    optimalni_troskovi = t

    # Mjesecna usteda
    cost_saving = np.subtract(standardni_troskovi, optimalni_troskovi).tolist()

    # Izrada tablice
    usporedba = {'standardni troskovi': standardni_troskovi, 'optimalni troskovi': optimalni_troskovi, 'mjesecna usteda': cost_saving}
    usporedba_troskova = pd.DataFrame(data=usporedba)
    usporedba_troskova.index = range(1, len(usporedba_troskova)+1)
    
    return(usporedba_troskova)




