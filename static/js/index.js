function toggleMenu() {
  let sidebar = document.getElementById("sidebar");
  if (sidebar.style.left === "0px") {
    sidebar.style.left = "-250px";
  } else {
    sidebar.style.left = "0px";
  }
}

function toggleDropdown() {
  let dropdownContent = document.getElementById("dropdownContent");
  if (dropdownContent.style.display === "block") {
    dropdownContent.style.display = "none";
  } else {
    dropdownContent.style.display = "block";
  }
}

function showModal(modalContent) {
  document.getElementById("Modal_Para").innerText = modalContent;
  document.getElementById("detailsModal").style.display = "flex";
}

function closeModal() {
  document.getElementById("detailsModal").style.display = "none";
}

function registerModal() {
  document.getElementById("registerModal").style.display = "flex";
}

function closeSignUpModal() {
  document.getElementById("registerModal").style.display = "none";
}

function registerModal(event) {
  let card = event.target.closest(".game-card");
  let eventName = card.querySelector("#Card_Head").innerText; // Get event name dynamically
  document.getElementById("registerModal").dataset.eventName = eventName;
  document.getElementById("registerModal").style.display = "flex";
}

document.getElementById("registerForm").addEventListener("submit", function (event) {
  event.preventDefault();

  let name = document.getElementById("name").value.trim();
  let email = document.getElementById("email").value.trim();
  let squad_name = document.getElementById("squad_name").value.trim();
  let squad_id = document.getElementById("squadid").value.trim();
  let phone = document.getElementById("phone").value.trim();
  let state = document.getElementById("state").value;
  let event_name = document.getElementById("registerModal").dataset.eventName; // Get event name

  if (!name || !email || !squad_name || !squad_id || !phone || !state) {
    alert("Please fill in all fields.");
    return;
  }

  // Show "Please wait" alert
  alert("Please wait while we process your registration...");

  fetch("/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: name,
      email: email,
      squad_name: squad_name,
      squad_id: squad_id,
      phone: phone,
      state: state,
      event_name: event_name, // Send event name
    }),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then(data => {
    alert(data.message);
    if (data.success) {
      closeSignUpModal();
    }
  })
  .catch((error) => {
    console.error("Error:", error);
    alert("Registration failed due to a network or server error. Please try again later.");
  });
});