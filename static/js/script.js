/* =========================================================
   VOYAGO — MAIN JAVASCRIPT
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* -----------------------------------------------------
       HEADER SCROLL EFFECT
    ----------------------------------------------------- */

    const header = document.getElementById("siteHeader");

    const updateHeader = () => {
        if (!header) return;

        if (window.scrollY > 50) {
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
        }
    };

    window.addEventListener("scroll", updateHeader, {
        passive: true
    });

    updateHeader();


    /* -----------------------------------------------------
       MOBILE MENU
    ----------------------------------------------------- */

    const mobileMenu = document.getElementById("mobileMenu");
    const navLinks = document.getElementById("navLinks");

    if (mobileMenu && navLinks) {

        mobileMenu.addEventListener("click", () => {

            navLinks.classList.toggle("mobile-open");

            mobileMenu.classList.toggle("active");

        });

        navLinks.querySelectorAll("a").forEach((link) => {

            link.addEventListener("click", () => {

                navLinks.classList.remove("mobile-open");
                mobileMenu.classList.remove("active");

            });

        });
    }


    /* -----------------------------------------------------
       SCROLL REVEAL
    ----------------------------------------------------- */

    const revealElements =
        document.querySelectorAll(".reveal");

    if ("IntersectionObserver" in window) {

        const observer = new IntersectionObserver(
            (entries, obs) => {

                entries.forEach((entry) => {

                    if (!entry.isIntersecting) return;

                    entry.target.classList.add("visible");

                    obs.unobserve(entry.target);

                });

            },
            {
                threshold: 0.12
            }
        );

        revealElements.forEach((element) => {
            observer.observe(element);
        });

    } else {

        revealElements.forEach((element) => {
            element.classList.add("visible");
        });

    }


    /* -----------------------------------------------------
       FAVORITE BUTTONS
    ----------------------------------------------------- */

    document
        .querySelectorAll(".favorite-button")
        .forEach((button) => {

            button.addEventListener("click", () => {

                button.classList.toggle("saved");

                button.textContent =
                    button.classList.contains("saved")
                        ? "♥"
                        : "♡";

            });

        });


    /* -----------------------------------------------------
       EXPLORE SEARCH & FILTER
    ----------------------------------------------------- */

    const searchInput =
        document.getElementById("destinationSearch");

    const filterButtons =
        document.querySelectorAll(".filter-button");

    const destinationCards =
        document.querySelectorAll(".explore-card");

    const noResults =
        document.getElementById("noResults");

    let selectedCategory = "all";


    const filterDestinations = () => {

        if (!destinationCards.length) return;

        const searchTerm =
            searchInput
                ? searchInput.value.toLowerCase().trim()
                : "";

        let visibleCount = 0;

        destinationCards.forEach((card) => {

            const name =
                (card.dataset.name || "").toLowerCase();

            const country =
                (card.dataset.country || "").toLowerCase();

            const category =
                (card.dataset.category || "").toLowerCase();

            const matchesSearch =
                name.includes(searchTerm) ||
                country.includes(searchTerm);

            const matchesCategory =
                selectedCategory === "all" ||
                category === selectedCategory;

            if (matchesSearch && matchesCategory) {

                card.style.display = "";
                visibleCount++;

            } else {

                card.style.display = "none";

            }

        });


        if (noResults) {

            noResults.style.display =
                visibleCount === 0
                    ? "block"
                    : "none";

        }

    };


    if (searchInput) {

        searchInput.addEventListener(
            "input",
            filterDestinations
        );

    }


    filterButtons.forEach((button) => {

        button.addEventListener("click", () => {

            filterButtons.forEach((item) => {
                item.classList.remove("active");
            });

            button.classList.add("active");

            selectedCategory =
                button.dataset.category || "all";

            filterDestinations();

        });

    });

});