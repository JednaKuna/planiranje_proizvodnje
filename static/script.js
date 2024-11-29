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


// Display results dynamically
function displayResults(result) {
  const resultsContainer = document.getElementById("results");
  

  // Clear previous results
  resultsContainer.innerHTML = "";

  // Add new results
  resultsContainer.innerHTML = `
          <h3>Results</h3>
          <p><strong>Total Cost (Fixed Demand):</strong> ${result.total_cost_fixed}e</p>
          <p><strong>Total Cost (Stochastic Demand):</strong> ${result.total_cost_stochastic}e</p>
          <h4>Graphs</h4>`;
          //<img src="data:image/png;base64,${results.graph1}" alt="Graph 1" style="max-width:100%; height:auto;" />
          //<img src="data:image/png;base64,${results.graph2}" alt="Graph 2" style="max-width:100%; height:auto;" />
          
}

// Initialize form with saved values on page load
document.addEventListener("DOMContentLoaded", () => {
  loadValues();
  generateInputs(); // Generate dynamic inputs if "time" was previously saved
});

// Attach submit handler to form
document.getElementById("wagner-form").addEventListener("submit", submitForm);