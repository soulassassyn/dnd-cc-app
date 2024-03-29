document.addEventListener("DOMContentLoaded", () => {
    const createBackstoryForm = document.getElementById("createBackstory");
    const selectRace = document.getElementById("charRace");
    const selectClass = document.getElementById("charClass");
    const raceInput = document.getElementById("race-input");
    const classInput = document.getElementById("class-input");

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
        //submit the form
        createBackstoryForm.submit();
    });
});