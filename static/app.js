document.addEventListener("DOMContentLoaded", () => {
    // Calculates and properly places the footer
    function checkHeight() {
        let totalHeight = 0;
        if (document.body.scrollHeight > window.innerHeight) {
            totalHeight = document.body.scrollHeight;
        } else {
            totalHeight = window.innerHeight;
        }
        document.documentElement.style.setProperty('--total-height', totalHeight + 'px');
    }
    
    window.onload = checkHeight;
    window.addEventListener("resize", checkHeight);
});