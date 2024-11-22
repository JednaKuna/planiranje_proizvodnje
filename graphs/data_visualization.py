import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def forecast_and_production(results_final):
    
    # Define values
    categories = results_final['period']
    forecast_values = results_final['forecast']
    production_values = results_final['production']

    # Number of bars
    n = len(categories)

    # Set the positions for the bars
    x = np.arange(n)

    # Bar width (adjust as needed)
    width = 0.35

    # Create the bars for 'forecast' and 'production' side by side
    plt.bar(x - width/2, forecast_values, width, label='Forecast')
    plt.bar(x + width/2, production_values, width, label='Production')
    plt.title('Comparison of Forecast and Production')
    plt.xlabel('Time')
    plt.ylabel('Quantity')
    plt.xticks(x, categories)
    plt.legend()
    plt.tight_layout()

    return(plt.show())

def inventory_and_production(results_final):
    
    categories = results_final['period']
    IOH_values = results_final['IOH']
    production_values = results_final['production']

    # Number of bars
    n = len(categories)

    # Set the positions for the bars
    x = np.arange(n)

    # Bar width (adjust as needed)
    width = 0.35

    # Create the bars for 'IOH' and 'production' side by side
    plt.bar(x + width/2, IOH_values, width, label='Inventory')
    plt.bar(x - width/2, production_values, width, label='Production')
    plt.title('Comparison of Inventory on hold and Production')
    plt.xlabel('Time')
    plt.ylabel('Quantity')
    plt.xticks(x, categories)
    plt.legend()
    plt.tight_layout()

    return(plt.show())

def normal_vs_optimal_costs(cost_comprison):
    
    # Create month labels based on the index of the DataFrame
    months = [str(i) for i in cost_comprison.index]

    # Plotting the line chart
    plt.figure(figsize=(10, 6))

    # Plot 'standardni_troskovi' and 'optimalni_troskovi'
    plt.plot(cost_comprison.index, cost_comprison['standardni troskovi'], label='Normal', marker='o')
    plt.plot(cost_comprison.index, cost_comprison['optimalni troskovi'], label='Optimal', marker='o')

    # Adding labels and title
    plt.title('Comparison of Normal vs Optimal Cost')
    plt.xlabel('Time')
    plt.ylabel('Cost')
    plt.xticks(cost_comprison.index, months)
    plt.legend()
    plt.tight_layout()
    
    return(plt.show())

def savings(cost_comparison):
    
    # Define a list to store the bar colors based on the 'mjesecna usteda' values
    bar_colors = ['red' if value < 0 else 'green' for value in cost_comparison['mjesecna usteda']]

    # Create a bar chart with conditional coloring
    plt.figure(figsize=(10, 6))
    bars = plt.bar(cost_comparison.index, cost_comparison['mjesecna usteda'], color=bar_colors)

    # Labeling the chart
    plt.title('Acumulation of savings over time')
    plt.xlabel('Time')
    plt.ylabel('Amount saved')
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

    plt.title('Total savings')
    plt.pie(pie, labels=[f"{x:.2f}e" for x in pie], autopct='%1.1f%%', colors=colors)

    return(plt.show())