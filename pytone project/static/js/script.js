document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded!");

    // Add to Cart using AJAX
    const addToCartButtons = document.querySelectorAll(".add-to-cart");
    addToCartButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const productId = this.getAttribute("data-id");

            fetch(`/add_to_cart/${productId}`)
                .then(response => response.json())
                .then(data => {
                    alert("Product added to cart!");
                    updateCartCount(data.cart_count);
                })
                .catch(error => console.error("Error:", error));
        });
    });

    // Update cart count
    function updateCartCount(count) {
        const cartCounter = document.getElementById("cart-count");
        if (cartCounter) {
            cartCounter.textContent = count;
        }
    }
});
