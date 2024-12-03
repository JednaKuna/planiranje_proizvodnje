//import Chart from 'chart.js/auto';

// Save form values to localStorage
function saveValues() {
  const form = document.getElementById("wagner-form");
  const formData = new FormData(form);

  for (const [key, value] of formData.entries()) {
    localStorage.setItem(key, value);
  }

  alert("Values saved!");
}

// Load saved values from localStorage on page load
function loadValues() {
  const form = document.getElementById("wagner-form");

  Array.from(form.elements).forEach((element) => {
    if (element.name && localStorage.getItem(element.name)) {
      if (element.type === "checkbox" || element.type === "radio") {
        element.checked = localStorage.getItem(element.name) === "true";
      } else {
        element.value = localStorage.getItem(element.name);
      }
    }
  });
}

// Generate dynamic input fields and load their values
function generateInputs() {
  const time = parseInt(document.getElementById("time").value, 10);
  const container = document.getElementById("dynamic-fields");

  container.innerHTML = ""; // Clear any existing fields

  if (!isNaN(time) && time > 0) {
    for (let i = 0; i < time; i++) {
      const label = document.createElement("label");
      label.textContent = `Quantity for Period ${i + 1}: `;
      const input = document.createElement("input");
      input.type = "number";
      input.name = `quantity[${i}]`;
      input.required = true;

      // Check localStorage for previously saved value
      const savedValue = localStorage.getItem(`quantity[${i}]`);
      if (savedValue) input.value = savedValue;

      container.appendChild(label);
      container.appendChild(input);
      container.appendChild(document.createElement("br"));
    }
  } else {
    alert("Please enter a valid positive number for Time.");
  }
}

// Submit form and fetch results from server
async function submitForm(event) {
  event.preventDefault(); // Prevent default form submission

  const form = document.getElementById("wagner-form");
  const formData = new FormData(form);
  

  // Create and serialize the quantities array
  const dynamicFields = document.querySelectorAll("#dynamic-fields input");
  const quantities = Array.from(dynamicFields).map((input) => parseFloat(input.value) || 0);
  formData.append("quantities", JSON.stringify(quantities)); // Add serialized array to FormData
  console.log('formData ', formData)
  console.log("Quantities array:", quantities);
  
  try {
    // Log formData for debugging
    for (let [key, value] of formData.entries()) {
      console.log(`${key}: ${value}`);
    }
  
    // Send POST request to server
    const response = await fetch("/calculate", {
      method: "POST",
      body: formData,
    });
  
    // Ensure the server responded successfully
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  
    const result = await response.json();
    console.log("Server Response:", result);
  
    // Handle response
    if (result.success) {
      displayResults(result);
    } else {
      alert("Error: " + (result.error || "Unknown error occurred"));
    }
  } catch (error) {
    console.error("Error submitting form:", error);
    alert("An error occurred. Please try again.");
  }
}


function displayResults(result) {
  const resultsContainer = document.getElementById("results");

  // Clear previous results
  resultsContainer.innerHTML = "";

  // Add new results
  resultsContainer.innerHTML = `
      <h3>Results</h3>
      <p><strong>Total Cost (Fixed Demand):</strong> ${result.total_cost_fixed}e</p>
      <p><strong>Total Cost (Stochastic Demand):</strong> ${result.total_cost_stochastic}e</p>
      <h4>Tables</h4>
      <h4>Stohastic demand</h4>
      <table id="df1" border="1">
      <thead>
          <tr id="table1-header"></tr>
      </thead>
          <tbody id="table1-body"></tbody>
      </table>
      <h4>Fixed demand</h4>
      <table id="df2" border="1">
      <thead>
          <tr id="table2-header"></tr>
      </thead>
          <tbody id="table2-body"></tbody>
      </table>
  `;
  // Table 1
  const tableHeader = document.getElementById('table1-header');
  const tableBody = document.getElementById('table1-body');

  try {
      const data = result.df1;

      if (data.length > 0) {
          // Create table headers
          const headers = Object.keys(data[0]);
          const reorderedHeaders = ["Period", ...headers.filter(header => header !== "Period")];
          reorderedHeaders.forEach(header => {
              const th = document.createElement('th');
              th.textContent = header;
              tableHeader.appendChild(th);
          });

          // Populate table rows
          data.forEach(row => {
              const tr = document.createElement('tr');
              reorderedHeaders.forEach(header => {
                  const td = document.createElement('td');
                  td.textContent = row[header];
                  tr.appendChild(td);
              });
              tableBody.appendChild(tr);
          });
      }
  } catch (error) {
      console.error("Error rendering table1:", error);
  }

  // Table 2
  const tableHeader2 = document.getElementById('table2-header');
  const tableBody2 = document.getElementById('table2-body');

  try {
      const data = result.df2;

      if (data.length > 0) {
          // Create table headers
          const headers = Object.keys(data[0]);
          const reorderedHeaders = ["Period", ...headers.filter(header => header !== "Period")];
          reorderedHeaders.forEach(header => {
              const th = document.createElement('th');
              th.textContent = header;
              tableHeader2.appendChild(th);
          });

          // Populate table rows
          data.forEach(row => {
              const tr = document.createElement('tr');
              reorderedHeaders.forEach(header => {
                  const td = document.createElement('td');
                  td.textContent = row[header];
                  tr.appendChild(td);
              });
              tableBody2.appendChild(tr);
          });
      }
  } catch (error) {
      console.error("Error rendering table2:", error);
  }

  // Create and append a canvas element for the chart
  const canvas = document.createElement("canvas");
  canvas.id = "myChart";
  resultsContainer.appendChild(canvas);

  // Prepare chart data
  //const graph1 = result.cumsum || {};
  //const labels = cumsum.period || [];
  //const values_fixed = graph1.values || [];
  const ctx = document.getElementById('myChart').getContext('2d');
  try {
    const data = result.cost_comparison;
    new Chart(ctx, {
      type: 'line', // Line chart type
      data: {
          labels: data.period, // X-axis labels (Periods)
          datasets: [
              {
                  label: 'Standard Costs',
                  data: data.standard, // Y-axis data
                  borderColor: 'rgba(75, 192, 192, 1)', // Line color
                  backgroundColor: 'rgba(75, 192, 192, 0.2)', // Fill color under line
                  tension: 0.3 // Smooth curve
              },
              {
                  label: 'Optimal Costs',
                  data: data.optimal, // Y-axis data
                  borderColor: 'rgba(54, 162, 235, 1)', // Line color
                  backgroundColor: 'rgba(54, 162, 235, 0.2)', // Fill color under line
                  tension: 0.3 // Smooth curve
              },
              {
                  label: 'Stohastic Costs',
                  data: data.stohastic, // Y-axis data
                  borderColor: 'rgba(255, 99, 132, 1)', // Line color
                  backgroundColor: 'rgba(255, 99, 132, 0.2)', // Fill color under line
                  tension: 0.3 // Smooth curve
              }
          ]
      },
      options: {
          responsive: true,
          plugins: {
              title: {
                  display: true,
                  text: 'Accumulation of Costs Over Time', // Chart title
                  font: {
                      size: 18
                  }
              },
              legend: {
                  display: true,
                  position: 'top' // Position of the legend
              }
          },
          scales: {
              x: {
                  title: {
                      display: true,
                      text: 'Period'
                  }
              },
              y: {
                  title: {
                      display: true,
                      text: 'Costs'
                  },
                  beginAtZero: false // Start y-axis from minimum cost
              }
          }
      }
  });
  } catch (error) {
    console.error("Error initializing Chart.js:", error);
  }
}
      

// Initialize form with saved values on page load
document.addEventListener("DOMContentLoaded", () => {
  loadValues();
  generateInputs(); // Generate dynamic inputs if "time" was previously saved
});

// Attach submit handler to form
document.getElementById("wagner-form").addEventListener("submit", submitForm);