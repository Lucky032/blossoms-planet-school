// Dashboard Loaded
document.addEventListener("DOMContentLoaded", function () {

    console.log("Dashboard Loaded Successfully!");

    // Highlight active sidebar menu
    const currentPath = window.location.pathname;

    document.querySelectorAll(".nav-link").forEach(function(link) {

        if (link.getAttribute("href") === currentPath) {

            link.classList.add("active");

        }

    });

});