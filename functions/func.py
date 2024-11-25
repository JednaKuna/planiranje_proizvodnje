import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def quantities_table(quantities, time):
    #Napraviti listu mjeseci, moguće generirati prema inputu
    period = [i for i in range(1, time+1)]

    #Napraviti popis količine narudžbi, moguće napumiti inputom
    forecast = quantities

    #Izrada dicitionaria od kojeg ću napraviti DataFrame
    d = {'Period': period, 'Forecast': forecast}

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
        current_month = data_calc.loc[index,'Period']
        cost = 0
        
        # Prva priprema
        cost += set_up
        if current_month > 1:
            for t in range(1, current_month+1):
                cost += (t-1) * data_calc.loc[t-1,'Forecast'] * holding
        data_calc.loc[index,'Order {}'.format(order)] = cost
    
    return (data_calc)

def other_orders(set_up, holding, data_calc, time_frame):
    
        # Ostale narudzbe
    for order in range(2, time_frame+1):
        for index, row in data_calc.iterrows():
            current_month = data_calc.loc[index,'Period']
            if current_month >= order:
                cost = 0

                # Najbolja opcija za prvi period
                values = list(data_calc.loc[order-2,['Order {}'.format(i) for i in range(1, order+1)]].values)
                best = min([i for i in values if i >0])

                # Zbrajanje
                cost += best + set_up
                for t in range(order, current_month+1):
                    cost += (t-order) * data_calc.loc[t-1,'Forecast'] * holding
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
       quantity = data[data['Period'].isin(range(next_id, initial_step+1))]['Forecast'].sum()
       
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
   #print("Total Cost: {:,}e".format(df_results.cost.sum()))
   
   return(df_results)
   
def calculation(setup_cost, hold_cost, production_cost, df_results, data):
    
    # Input data
    results_final = data.copy()

    # Proizvodnja
    month_prod = df_results['nexts'].values
    prod_dict = dict(zip(month_prod, df_results.quantity.values))

    # Values
    results_final['Production'] = results_final['Period'].apply(lambda t: prod_dict[t] if t in month_prod else 0)

    # Inventory On Hand
    results_final['Inventory on Hold'] = (results_final['Production'] - results_final['Forecast']).cumsum()

    # Holding Cost
    results_final['Holding Cost'] = (results_final['Inventory on Hold'] * hold_cost)

    # Set Up Cost
    results_final['Set-Up Costs'] = results_final['Production'].apply(lambda t: setup_cost if t > 0 else 0)

    # Holding + Set-Up
    #results_final['Holding + Set-Up'] = results_final[['Holding Cost', 'Set-Up Costs']].sum(axis = 1)

    # Ukupno 
    results_final['Total Costs(inc. Production)'] = (results_final['Production'] * production_cost) + results_final['Set-Up Costs'] + results_final['Holding Cost']

    return(results_final)


    
def cost_comparison(setup_cost, production_cost, holding_cost, time_frame, results_final, detailed_schedule_df_no_leftovers):
    
    #Izračum ukupnih troškova tjekom odabranog perioda
    # Standardni troskovi: tu sam racunao samo troskove pripreme (bez troskova skladistenja)
    s = [0] * time_frame
    s[0]= setup_cost

    for i in range(1,time_frame):
        s[i] = (s[i-1] + setup_cost)
        
    ss = [i * production_cost for i in results_final['Forecast'].tolist()]
    
    for i in range(1,time_frame):
        ss[i] = (ss[i] + ss[i-1])

    standardni_troskovi = np.add(s,ss).tolist()

    #Optimalni troskovi
    optimalni_troskovi = results_final['Total Costs(inc. Production)'].tolist()
    t = [0] * time_frame
    t[0] = optimalni_troskovi[0]

    for i in range(0,time_frame):
        t[i] = t[i-1] + optimalni_troskovi[i]
    optimalni_troskovi = t
    
    # Stohastički troškovi
    
    stohasticki_troskovi = np.cumsum(detailed_schedule_df_no_leftovers['Total Costs(inc. Production)'])

    

    # Mjesecna usteda
    cost_saving1 = np.subtract(standardni_troskovi, optimalni_troskovi).tolist()
    cost_saving2 = np.subtract(standardni_troskovi, stohasticki_troskovi).tolist()

    # Izrada tablice
    usporedba = {'Standard Costs': standardni_troskovi, 'Optimal Costs': optimalni_troskovi, 'Stohastic Costs': stohasticki_troskovi, 'Monthly Savings Normal': cost_saving1, 'Monthly Savings Stohastic Method': cost_saving2}
    usporedba_troskova = pd.DataFrame(data=usporedba)
    usporedba_troskova.index = range(1, len(usporedba_troskova)+1)
    
    return(usporedba_troskova)


# Stohasticki pristup


def create_detailed_schedule(schedule, quantity_per_period, time_period, setUp_cost, holding_cost, production_cost):
    data = {
        "Period": list(range(1, time_period + 1)),
        "Forecast": quantity_per_period,
        "Production": [0] * time_period,
        "Inventory on Hold": [0] * time_period,
        "Holding Costs": [0] * time_period,
        "Set-Up Costs": [0] * time_period,
        "Total Costs(inc. Production)": [0] * time_period,
    }

    inventory = 0  # Track inventory on hold

    for start, end, production_quantity in schedule:
        # Record production in the starting period
        data["Production"][start - 1] = production_quantity
        data["Set-Up Costs"][start - 1] = setUp_cost

        # Distribute inventory and calculate costs
        for period in range(start, end + 1):
            demand = quantity_per_period[period - 1]
            # Use inventory and new production to meet demand
            available = inventory + (production_quantity if period == start else 0)
            inventory = max(0, available - demand)  # Remaining inventory
            production_quantity = max(0, production_quantity - demand)

            data["Inventory on Hold"][period - 1] = inventory
            data["Holding Costs"][period - 1] = inventory * holding_cost
            data["Total Costs(inc. Production)"][period - 1] = (inventory * holding_cost) + data["Set-Up Costs"][period - 1] + (data["Production"][period - 1] * production_cost)        

    return pd.DataFrame(data)


def create_detailed_schedule_no_leftovers(schedule, quantity_per_period, time_period, setUp_cost, holding_cost, production_cost):
    data = {
        "Period": list(range(1, time_period + 1)),
        "Forecast": quantity_per_period,
        "Production": [0] * time_period,
        "Inventory on Hold": [0] * time_period,
        "Holding Costs": [0] * time_period,
        "Set-Up Costs": [0] * time_period,
        "Total Costs(inc. Production)": [0] * time_period,
    }

    inventory = 0  # Track inventory on hold

    for start, end, production_quantity in schedule:
        # Adjust final production to avoid leftovers
        if end == time_period:
            production_quantity = sum(quantity_per_period[start - 1:end]) - inventory
        
        # Record production in the starting period
        data["Production"][start - 1] = production_quantity
        data["Set-Up Costs"][start - 1] = setUp_cost if production_quantity > 0 else 0

        # Distribute inventory and calculate costs
        for period in range(start, end + 1):
            demand = quantity_per_period[period - 1]
            # Use inventory and new production to meet demand
            available = inventory + (production_quantity if period == start else 0)
            inventory = max(0, available - demand)  # Remaining inventory
            production_quantity = max(0, production_quantity - demand)

            data["Inventory on Hold"][period - 1] = inventory
            data["Holding Costs"][period - 1] = inventory * holding_cost
            data["Total Costs(inc. Production)"][period - 1] = (
                data["Holding Costs"][period - 1] +
                data["Set-Up Costs"][period - 1] +
                (data["Production"][period - 1] * production_cost)
            )

    return pd.DataFrame(data)




def wagner(normal_scenarios_with_safety_stock, time_period, setUp_cost, holding_cost):

    # Store results
    costs_normal = []
    optimal_schedules_normal = []

    # Apply Wagner-Whitin for each normal distribution scenario
    for scenario in normal_scenarios_with_safety_stock:
        # Reset variables for each scenario
        F = [float('inf')] * (time_period + 1)
        F[0] = 0
        C = [[0] * time_period for _ in range(time_period)]

        # Recompute the cost matrix C(i, j)
        for i in range(1, time_period + 1):
            total_holding = 0
            total_quantity = 0
            for j in range(i, time_period + 1):
                total_quantity += scenario[j - 1]
                if j > i:
                    total_holding += (j - i) * scenario[j - 1]
                C[i - 1][j - 1] = setUp_cost + holding_cost * total_holding

        # Compute the minimum cost F(j)
        for j in range(1, time_period + 1):
            for i in range(1, j + 1):
                F[j] = min(F[j], F[i - 1] + C[i - 1][j - 1])

        # Backtrack to find the optimal production schedule
        production_schedule = []
        j = time_period
        while j > 0:
            for i in range(1, j + 1):
                if F[j] == F[i - 1] + C[i - 1][j - 1]:
                    production_schedule.append((i, j, sum(scenario[i - 1:j])))
                    j = i - 1
                    break

        # Reverse the schedule to chronological order
        production_schedule.reverse()

        # Store results for this scenario
        costs_normal.append(F[-1])
        optimal_schedules_normal.append(production_schedule)
        
    return(costs_normal, optimal_schedules_normal)

