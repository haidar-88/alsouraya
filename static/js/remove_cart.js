  document.addEventListener('DOMContentLoaded', () => {

  const cart = document.getElementById('cart');

  cart.addEventListener('click', event => {
    if (event.target.classList.contains('remove-from-cart')) {
      const button = event.target;
      const productId = button.getAttribute('data-product-id');
      
      const cartItem = event.target.closest('.cart-item');
      const productSize = cartItem.querySelector('.size').textContent.trim();
      const productColor = cartItem.querySelector('.color').textContent.trim();

      fetch('https://alsouraya.onrender.com/remove-from-cart', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, size: productSize, color: productColor})
      })
      .then(res => {
        if (res.ok) {
          // Remove the item from the DOM
          alert('Product Removed from cart');
          location.reload(true);
        } else {
          alert('Failed to remove from cart.');
        }
      })
      .catch(err => {
        console.error('Remove from cart error:', err);
        alert('Error removing from cart.');
      });
    }
  });

});