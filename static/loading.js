document.addEventListener("DOMContentLoaded", () => {
    // Loading button
    let button = document.getElementById("createButton");
    button.onclick = function(event) {
        event.preventDefault();
        let form = button.closest('form');
        button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
        button.setAttribute("disabled", true);
        form.submit();
    }
});