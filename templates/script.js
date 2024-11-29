

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

  // Add dynamic fields to FormData
  const dynamicFields = document.querySelectorAll("#dynamic-fields input");
  dynamicFields.forEach((input) => {
    formData.append(input.name, input.value);
  });

  try {
    // Send POST request to server
    const response = await fetch("/calculate", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    // Handle response
    if (result.success) {
      displayResults(result);
    } else {
      alert("Error: " + result.error);
    }
  } catch (error) {
    console.error("Error submitting form:", error);
    alert("An error occurred. Please try again.");
  }
}

// Display results dynamically
function displayResults(data) {
  const resultsContainer = document.getElementById("results");

  // Clear previous results
  resultsContainer.innerHTML = "";

  // Add new results
  resultsContainer.innerHTML = `
          <h3>Results</h3>
          <p><strong>Total Cost (Fixed Demand):</strong> ${data.total_cost_fixed_demand}€</p>
          <p><strong>Total Cost (Stochastic Demand):</strong> ${data.total_cost_stochastic_demand}€</p>
        `;
}

// Initialize form with saved values on page load
document.addEventListener("DOMContentLoaded", () => {
  loadValues();
  generateInputs(); // Generate dynamic inputs if "time" was previously saved
});

// Attach submit handler to form
document.getElementById("wagner-form").addEventListener("submit", submitForm);
