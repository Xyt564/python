// Sidebar arrow key navigation with independent scrolling
document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.querySelector(".sidebar");
    const items = Array.from(sidebar.querySelectorAll("a"));
    let currentIndex = items.findIndex(i => i.classList.contains("active"));

    document.addEventListener("keydown", function(event) {
        if (items.length === 0) return;

        if (event.key === "ArrowDown") {
            currentIndex = (currentIndex + 1) % items.length;
            items[currentIndex].focus();

            // Scroll sidebar only
            const itemTop = items[currentIndex].offsetTop;
            const itemBottom = itemTop + items[currentIndex].offsetHeight;
            if (itemBottom > sidebar.scrollTop + sidebar.clientHeight) {
                sidebar.scrollTop = itemBottom - sidebar.clientHeight;
            } else if (itemTop < sidebar.scrollTop) {
                sidebar.scrollTop = itemTop;
            }

            event.preventDefault();
        } else if (event.key === "ArrowUp") {
            currentIndex = (currentIndex - 1 + items.length) % items.length;
            items[currentIndex].focus();

            const itemTop = items[currentIndex].offsetTop;
            const itemBottom = itemTop + items[currentIndex].offsetHeight;
            if (itemBottom > sidebar.scrollTop + sidebar.clientHeight) {
                sidebar.scrollTop = itemBottom - sidebar.clientHeight;
            } else if (itemTop < sidebar.scrollTop) {
                sidebar.scrollTop = itemTop;
            }

            event.preventDefault();
        }
    });
});
