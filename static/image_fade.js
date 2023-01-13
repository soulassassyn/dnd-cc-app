document.addEventListener("DOMContentLoaded", () => {
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
    }, 5000);
});