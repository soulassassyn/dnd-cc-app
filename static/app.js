document.addEventListener("DOMContentLoaded", () => {
    var currentPage = 1;
    function goToNextPage() {
        currentPage++;
        window.location.href = "create0" + currentPage + ".html";
    }
    function goToLastPage() {
        currentPage--;
        window.location.href = "create0" + currentPage + ".html";
    }
    // Add event listener to the buttons
    var nextBtn = document.getElementById("next-button");
    var backBtn = document.getElementById("back-button");
    nextBtn.addEventListener("click", goToNextPage);
    backBtn.addEventListener("click", goToLastPage);
});


