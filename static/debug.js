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