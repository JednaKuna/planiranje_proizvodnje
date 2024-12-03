from flask import Flask, request, render_template, jsonify
import numpy as np
import utils.functions.func as f
import utils.graphs.data_visualization as data_viz
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = True  # Enables debug mode
app.config['USE_PIN'] = False  # Disables pin for local debugging

# Service Level Z-Scores
ssc = {
    0.70: 0.524, 0.75: 0.674, 0.80: 0.842, 0.81: 0.878, 0.82: 0.915, 0.83: 0.954, 0.84: 0.994, 0.85: 1.036, 
    0.86: 1.080, 0.87: 1.126, 0.88: 1.175, 0.89: 1.227, 0.90: 1.282, 0.91: 1.341, 0.92: 1.405, 0.93: 1.476, 
    0.94: 1.555, 0.95: 1.645, 0.96: 1.751, 0.97: 1.881, 0.98: 2.054, 0.99: 2.326, 0.995: 2.576
}

@app.route("/")
def index():
    # Serve the form to collect user inputs
    return render_template("index.html")  # Place your HTML file in the 'templates' folder

@app.route("/calculate", methods=["POST"])
def calculate():
    # Extract form data
    try:
        # Get the time period and quantities
        time_period = int(request.form['time'])
        quantities_json = request.form.get('quantities')  # Get the serialized JSON string
        quantities = json.loads(quantities_json)
         # Ensure quantities length matches time period
        if len(quantities) != time_period:
            return jsonify({"success": False, "error": f"Number of quantities({len(quantities)}) does not match the time period({time_period})."})

        # Convert quantities to integers
        quantities = [int(q) for q in quantities]
        quantity_per_period = quantities

        # Other form values
        
        setUp_cost = float(request.form.get("Set-Up Cost", 500))
        holding_cost = float(request.form.get("holding cost", 1))
        production_cost = float(request.form.get("production", 3))
        service_level = float(request.form.get("service", 0.92))
        mean_demand_shift = float(request.form.get("mean", 0))
        std_dev_demand = float(request.form.get("dev", 5))
        num_scenarios = int(request.form.get("scenarios", 1000))

        # Ensure quantities match the time period
        if len(quantity_per_period) != time_period:
            return jsonify({"error": "Number of quantities does not match the time period."}), 400

        # Proceed with calculations using quantity_per_period
        # Generate stochastic demand scenarios
        normal_scenarios = np.random.normal(
            mean_demand_shift, std_dev_demand, (num_scenarios, time_period)
            ) + quantity_per_period
        normal_scenarios = np.clip(normal_scenarios, 0, None).astype(int)

        # Calculate safety stock
        z_score = ssc[service_level]
        safety_stock = np.ceil(z_score * std_dev_demand).astype(int)
        normal_scenarios_with_safety_stock = normal_scenarios + safety_stock

        # Apply Wagner-Whitin method
        costs_normal, optimal_schedules_normal = f.wagner(
            normal_scenarios_with_safety_stock, time_period, setUp_cost, holding_cost
        )

        # Average cost and optimal schedule
        average_cost_normal = np.mean(costs_normal)
        optimal_schedule_summary_normal = optimal_schedules_normal[np.argmin(costs_normal)]

        # Calculate costs for Wagner-Whitin method
        costs, schedule=f.wagner2(quantity_per_period, time_period, setUp_cost, holding_cost)
        schedule_summary=schedule[np.argmin(costs)]
        results_final = f.create_detailed_schedule(schedule_summary, quantity_per_period, time_period, setUp_cost, holding_cost, production_cost)

        # Detailed stochastic schedule
        detailed_schedule_df_no_leftovers = f.create_detailed_schedule_no_leftovers(
            optimal_schedule_summary_normal, quantity_per_period, time_period, setUp_cost, holding_cost, production_cost
        )

        # Cumulative sum of costs
        cumsum1 = results_final["Total Costs(inc. Production)"].cumsum().tolist()
        cumsum2 = detailed_schedule_df_no_leftovers["Total Costs(inc. Production)"].cumsum().tolist()
        cumsum = {
            "period": [i for i in range(1, len(quantity_per_period)+1)],
            "fixed": cumsum1,
            "stohastic": cumsum2
        }
        
        # Costs Comparison DataFrame and Dict for graph
        cost_comparison_df=f.cost_comparison(setUp_cost, production_cost, holding_cost, time_period, results_final, detailed_schedule_df_no_leftovers)
        cost_comparison = {
            "period": [i for i in range(1, len(quantity_per_period)+1)],
            "standard": cost_comparison_df["Standard Costs"].tolist(),
            "optimal": cost_comparison_df["Optimal Costs"].tolist(),
            "stohastic": cost_comparison_df["Stohastic Costs"].tolist(),
        }
        
        total_cost1 = int(results_final["Total Costs(inc. Production)"].sum())
        total_cost2 = int(detailed_schedule_df_no_leftovers["Total Costs(inc. Production)"].sum())

        # Generate graphs
        # Production quantity
        graph1 = {
                "labels": [i for i in range(1, len(quantity_per_period)+1)],
                "values": quantity_per_period,
            }
        
        # Summarize the response
        return jsonify({
            "success": True,
            "total_cost_fixed": total_cost1,
            "total_cost_stochastic": total_cost2,
            "average_cost_normal": average_cost_normal,
            "quantity_per_period": quantity_per_period,  # Include for debugging or confirmation
            "graph1": graph1,  
            "df1": detailed_schedule_df_no_leftovers.to_dict(orient='records'),
            "df2": results_final.to_dict(orient='records'),
            "cumsum": cumsum,
            "cost_comparison": cost_comparison

        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
