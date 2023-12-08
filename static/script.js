document.addEventListener("DOMContentLoaded", function () {
    const banner = document.getElementById("banner");
    const dotsContainer = document.getElementById("dots-container");

    let currentIndex = 0;
    const slides = document.querySelectorAll(".slide");

    // Crea los puntos (dots) según la cantidad de slides
    slides.forEach((_, index) => {
        const dot = document.createElement("div");
        dot.classList.add("dot");
        dot.addEventListener("click", () => showSlide(index));
        dotsContainer.appendChild(dot);
    });

    // Inicia el intervalo para cambiar las imágenes cada 4 segundos
    setInterval(() => showNextSlide(), 4000);

    function showNextSlide() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    }

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.transform = `translateX(${-index * 100}%)`;
            const dot = dotsContainer.children[i];
            dot.classList.toggle("active", i === index);
        });
    }
});

document.querySelector(".menu-toggle").addEventListener("click", function () {
    document.querySelector(".sidebar").style.width = "250px";
});

document.querySelector(".sidebar-close").addEventListener("click", function () {
    document.querySelector(".sidebar").style.width = "0";
});

