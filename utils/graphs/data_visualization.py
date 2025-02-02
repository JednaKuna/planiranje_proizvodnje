import pandas as pd
import numpy as np
import io
import base64
import matplotlib
import matplotlib.pyplot as plt





def forecast_and_production(results_final, detailed_schedule_df_no_leftovers):
    
    # Define values
    categories = results_final['Period']
    forecast_values = results_final['Forecast']
    production_values1 = results_final['Production']
    production_values2 = detailed_schedule_df_no_leftovers['Production']
    buf1 = io.BytesIO()
    # Number of bars
    n = len(categories)

    # Set the positions for the bars
    x = np.arange(n)

    # Bar width (adjust as needed)
    width = 0.25

    # Create the bars for 'forecast' and 'production' side by side
    plt.bar(x - width, forecast_values, width, label='Naručene količine')
    plt.bar(x, production_values1, width, label='Fiksne količine')
    plt.bar(x + width, production_values2, width, label='Promjenjive količine')
    plt.title('Usporedba naručenih i proizvedenih količina')
    plt.xlabel('Vrijeme')
    plt.ylabel('Količina')
    plt.xticks(x, categories)
    plt.legend()
    plt.tight_layout()
    #plt.savefig(buf1, format="png") 
    #buf1.seek(0)
    #plt.close()
    #graph1_base64 = base64.b64encode(buf1.getvalue()).decode("utf-8")
    return(plt.show())

def inventory(results_final, detailed_schedule_df_no_leftovers):
    
    # Define values
    categories = results_final['Period']
    forecast_values = results_final['Forecast']
    inventory_values1 = results_final['Inventory on Hold']
    inventory_values2 = detailed_schedule_df_no_leftovers['Inventory on Hold']
    buf1 = io.BytesIO()

    # Number of bars
    n = len(categories)

    # Set the positions for the bars
    x = np.arange(n)

    # Bar width (adjust as needed)
    width = 0.25

    # Create the bars for 'forecast' and 'inventory' side by side
    plt.bar(x - width, forecast_values, width, label='Naručene količine')
    plt.bar(x, inventory_values1, width, label='Fiksna potražnja')
    plt.bar(x + width, inventory_values2, width, label='Promjenjiva potražnja')
    plt.title('Usporedba naručenih količina i stanja skladišta')
    plt.xlabel('Vrijeme')
    plt.ylabel('Količina')
    plt.xticks(x, categories)
    plt.legend()
    plt.tight_layout()
    plt.savefig(buf1, format="png")
    buf1.seek(0)
    #plt.close()
    #graph1_base64 = base64.b64encode(buf1.getvalue()).decode("utf-8")
    return(plt.show())

def normal_vs_optimal_costs(cost_comprison):
    
    # Create month labels based on the index of the DataFrame
    months = [str(i) for i in cost_comprison.index]

    # Plotting the line chart
    plt.figure(figsize=(10, 6))

    # Plot 'standardni_troskovi' and 'optimalni_troskovi'
    plt.plot(cost_comprison.index, cost_comprison['Standard Costs'], label='Normal', marker='o')
    plt.plot(cost_comprison.index, cost_comprison['Optimal Costs'], label='Optimal', marker='o')
    plt.plot(cost_comprison.index, cost_comprison['Stohastic Costs'], label='Stohastic', marker='o')

    # Adding labels and title
    plt.title('Usporedba troškova')
    plt.xlabel('Vrijeme')
    plt.ylabel('Troškovi')
    plt.xticks(cost_comprison.index, months)
    plt.legend()
    plt.tight_layout()
    
    return(plt.show())

def savings(cost_comparison):
    
    # Define a list to store the bar colors based on the 'mjesecna usteda' values
    bar_colors = ['red' if value < 0 else 'green' for value in cost_comparison['Monthly Savings Stohastic Method']]

    # Create a bar chart with conditional coloring
    plt.figure(figsize=(10, 6))
    bars = plt.bar(cost_comparison.index, cost_comparison['Monthly Savings Stohastic Method'], color=bar_colors)

    # Labeling the chart
    plt.title('Akumulacija uštede')
    plt.xlabel('Vrijeme')
    plt.ylabel('Količina uštede')
    plt.xticks(cost_comparison.index)  # Show all x-axis ticks for each index

    # Annotate each bar with its value
    for bar in bars:
        # Get the height of the bar (the value of 'mjesecna usteda')
        height = bar.get_height()
        
        plt.text(bar.get_x() + bar.get_width() / 2, height + (50),  
                f'{height:.2f}e', ha='center', va='center', fontsize=10, color='black')

    return(plt.show())

def usteda(optimal_costs, cost_saving):
    # Data
    pie = [optimal_costs, cost_saving]
    colors = ['lightgray', 'green']

    plt.title('Ukupna ušteda')
    plt.pie(pie, labels=[f"{x:.2f}e" for x in pie], autopct='%1.1f%%', colors=colors)

    return(plt.show())