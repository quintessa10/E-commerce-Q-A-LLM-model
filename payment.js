document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const amount = urlParams.get('amount') || 0;
    document.getElementById('payment-amount').innerText = amount;

    const paymentForm = document.getElementById('payment-form');
    paymentForm.addEventListener('submit', function (e) {
        e.preventDefault();
        
        // Simulate payment processing
        const cardNumber = document.getElementById('card-number').value;
        const expiryDate = document.getElementById('expiry-date').value;
        const cvv = document.getElementById('cvv').value;

        // Here you would normally process the payment with a payment gateway
        // For this simulation, we'll just display a success message
        if (cardNumber && expiryDate && cvv) {
            document.getElementById('payment-message').innerText = 'Payment successful! Thank you for your purchase.';
        } else {
            document.getElementById('payment-message').innerText = 'Please fill in all fields.';
        }
    });
});

let cart = JSON.parse(localStorage.getItem('cart')) || [];

function addToCart(itemName, price) {
    cart.push({ name: itemName, price: price });
    localStorage.setItem('cart', JSON.stringify(cart));
    alert(`${itemName} has been added to your cart!`);
    loadCart(); // Refresh the cart view
}

function removeFromCart(index) {
    cart.splice(index, 1); // Remove the item at the given index
    localStorage.setItem('cart', JSON.stringify(cart));
    loadCart(); // Refresh the cart view
}

function loadCart() {
    if (document.getElementById('cart-items')) { // Only load if on cart.html
        let cartItemsDiv = document.getElementById('cart-items');
        let totalAmount = 0;
        cartItemsDiv.innerHTML = '';

        cart.forEach((item, index) => {
            cartItemsDiv.innerHTML += `
                <div class="cart-item">
                    <h4>${item.name}</h4>
                    <p>₹${item.price}</p>
                    <button onclick="removeFromCart(${index})">Remove</button>
                </div>`;
            totalAmount += item.price;
        });

        document.getElementById('total-amount').innerText = totalAmount;
    }
}

document.addEventListener("DOMContentLoaded", loadCart);
