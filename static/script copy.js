const images = document.querySelectorAll(".slideshow img");
const imageCount = images.length;
let currentImage = 0;

setInterval(() => {
    images[currentImage].style.display = "none";
    currentImage = (currentImage + 1) % imageCount;
    images[currentImage].style.display = "block";
}, 3000);
