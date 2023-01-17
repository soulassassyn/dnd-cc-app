document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registration-form");
    const password = document.getElementById("password");
    const password_confirmation = document.getElementById("password_confirmation");
  
    form.addEventListener("submit", function(event) {
      if (password.value !== password_confirmation.value) {
        alert("Passwords do not match!");
        event.preventDefault();
      }
    });
});