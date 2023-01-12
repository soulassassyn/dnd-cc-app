document.addEventListener("DOMContentLoaded", () => {
    const checkbox = document.getElementById("switch-button");
    const state = document.getElementById("switch-state");
    const toggle = document.getElementById("toggle");
    const charSex = document.getElementById("charSexM");
    const charRace = document.getElementById("charRace");
    const charClass = document.getElementById("charClass");
    const charName = document.getElementById("charName");
    const q1 = document.getElementById("q1a4");
    const q2 = document.getElementById("q2a1");
    const q3 = document.getElementById("q3a1");
    const q4 = document.getElementById("q4a4");
    const q5 = document.getElementById("q5a4");
    const q6 = document.getElementById("q6a1");
    const createBackstoryForm = document.getElementById("createBackstory");
    const selectRace = document.getElementById("charRace");
    const selectClass = document.getElementById("charClass");
    const selectBackground = document.getElementById("charBackground");
    const raceInput = document.getElementById("race-input");
    const classInput = document.getElementById("class-input");
    const backgroundInput = document.getElementById("background-input");


    // Add an event listener to the race select menu
    selectRace.addEventListener("change", function() {
        // Check if the "Custom......" option is selected
        if (selectRace.value === "Custom...") {
            // Show the text input
            raceInput.style.display = "block";
            raceInput.required = true;
        } else {
            // Hide the text input
            raceInput.style.display = "none";
            raceInput.required = false;
        }
    });

    // Add an event listener to the class select menu
    selectClass.addEventListener("change", function() {
        // Check if the "Custom......" option is selected
        if (selectClass.value === "Custom...") {
            // Show the text input
            classInput.style.display = "block";
            classInput.required = true;
        } else {
            // Hide the text input
            classInput.style.display = "none";
            classInput.required = false;
        }
    });

    // Add an event listener to the class select menu
    selectBackground.addEventListener("change", function() {
        // Check if the "Custom......" option is selected
        if (selectBackground.value === "Custom...") {
            // Show the text input
            backgroundInput.style.display = "block";
            backgroundInput.required = true;
        } else {
            // Hide the text input
            backgroundInput.style.display = "none";
            backgroundInput.required = false;
        }
    });

    // Add an event listener to the form's submit button
    createBackstoryForm.addEventListener("submit", function(e) {
        //prevent default form submission
        e.preventDefault();
        // Check if the "Custom......" option is selected
        if (charRace.value === "Custom...") {
            // Update the value of the select menu to the text entered in the text box
            charRace.value = raceInput.value;
        }
        if (charClass.value === "Custom...") {
            // Update the value of the select menu to the text entered in the text box
            charClass.value = classInput.value;
        }
        if (charBackground.value === "Custom...") {
            // Update the value of the select menu to the text entered in the text box
            charBackground.value = backgroundInput.value;
        }
        //submit the form
        createBackstoryForm.submit();
    });

    // Loads all of the portrait images into the 'images' variable
    const images = document.querySelectorAll("#portrait-container img");
    let currentImageIndex = 0;
    
    setInterval(() => {
      // Fade out the current image
      images[currentImageIndex].style.opacity = 0;
    
      // Increment the current image index, and set it back to 0 if it's the last image
      currentImageIndex = (currentImageIndex + 1) % images.length;
    
      // Fade in the new image
      images[currentImageIndex].style.opacity = 1;
    }, 3500);
    

    // function for the API toggle
    checkbox.addEventListener("change", function() {
        // Send an HTTP POST request to the /switch route
        fetch("/switch", {method: "POST"})
            .then(response => response.text())
            .then(text => {
            // Update the displayed state of the switch
            state.textContent = text;
            });
    });

    // function for the Autofill toggle
    toggle.addEventListener("change", function() {
        const questions = [q1, q2, q3, q4, q5, q6];
        if (toggle.checked) {
            // If the toggle is checked, autofill the form fields
            charSex.checked = true;
            charRace.value = "Human";
            charClass.value = "Paladin";
            charName.value = "Barriston";
            for (const q of questions){
                q.checked = true;
            }
        } else {
            // If the toggle is not checked, clear the form fields
            charSex.checked = false;
            charRace.value = "";
            charClass.value = "";
            charName.value = "";
            for (const q of questions){
                q.checked = false;
            }
        }
    });
});


