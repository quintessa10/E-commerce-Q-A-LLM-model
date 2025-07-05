let cart = JSON.parse(localStorage.getItem('cart')) || [];

function addToCart(itemName, price) {
    cart.push({ name: itemName, price: price });
    localStorage.setItem('cart', JSON.stringify(cart));
    alert(`${itemName} has been added to your cart!`);
}

function loadCart() {
    let cartItems = JSON.parse(localStorage.getItem('cart')) || [];
    let cartDiv = document.getElementById('cart-items');
    let totalAmount = 0;

    cartItems.forEach(item => {
        cartDiv.innerHTML += `<p>${item.name} - ₹${item.price}</p>`;
        totalAmount += item.price;
    });

    document.getElementById('total-amount').innerText = totalAmount;
}

document.addEventListener("DOMContentLoaded", loadCart);

function checkout() {
    var totalAmount = document.getElementById('total-amount').innerText;

    var options = {
        key: 'YOUR_RAZORPAY_KEY', // Enter the Key ID generated from the Razorpay Dashboard
        amount: totalAmount * 100, // Amount is in currency subunits. Hence, 100 paise = 1 INR
        currency: 'INR',
        name: 'Your Company Name',
        description: 'Purchase Description',
        image: 'https://example.com/your_logo', // Optional
        order_id: '', // Use the generated order_id from your server
        handler: function (response) {
            alert('Payment successful! Payment ID: ' + response.razorpay_payment_id);
            // You can redirect the user to a success page or update your database here
        },
        prefill: {
            name: '',
            email: '',
            contact: ''
        },
        notes: {
            address: ''
        },
        theme: {
            color: '#F37254'
        }
    };

    var rzp1 = new Razorpay(options);
    rzp1.open();
}
