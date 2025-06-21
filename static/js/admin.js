
const categorySelect = document.getElementById('category-filter');
const productList = document.getElementById('product-list');


productList.addEventListener('click', event => { //delete prdct
if (event.target.classList.contains('delete-product')) {
    const button = event.target;
    const productId = button.getAttribute('data-product-id');

    fetch('https://alsouraya.onrender.com/delete-product', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: productId })
    })
    .then(res => {
    if (res.ok) {
        alert('Product Deleted');
        location.reload(true);
    } else {
        alert('Failed to delete product.');
    }
    })
    .catch(err => {
    console.error('delete product error:', err);
    alert('Error deleting product.');
    });
}
});

productList.addEventListener('click', event => { //update prdct
if (event.target.classList.contains('update-product')) {
    const button = event.target;
    const productId = button.getAttribute('data-product-id');

    alert('not functional waiting for update')
    return 0;
    fetch('https://alsouraya.onrender.com/update-product', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: productId })
    })
    .then(res => {
    if (res.ok) {
        alert('Product Deleted');
    } else {
        alert('Failed to delete product.');
    }
    })
    .catch(err => {
    console.error('delete product error:', err);
    alert('Error deleting product.');
    });
}
});


categorySelect.addEventListener('change', () => { //filter
const selectedCategory = categorySelect.value;

fetch('https://alsouraya.onrender.com/admin-filter-product', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ category: selectedCategory })
})
.then(res => res.json())
.then(products => {
    // Replace product list HTML
    productList.innerHTML = products.map(buildProductCard).join('');
})
.catch(err => {
    console.error('Error fetching filtered products:', err);
});
});


function buildProductCard(product) { //build after filter
  return `
    <div class="product-card">
      <h3>${product.category}</h3>

      <div class="product-details">
        <div class="product-info">
          <p>Sizes:</p>
          <div class="size-options">
            ${product.sizes.map(size => `
              <button class="size-option" data-size="${size}">${size}</button>
            `).join('')}
          </div>

          <p>Colors:</p>
          <div class="color-options">
            ${product.colors.map(color => `
              <button class="color-option" data-color="${color}">${color}</button>
            `).join('')}
          </div>

          <p>$${product.unit_price}</p>
        </div>

        <div class="product-image">
          <img src="${product.image_path[0]}" alt="Product Image">
        </div>
      </div>

      <button class="delete-product" data-product-id="${product.product_id}">Delete Product</button>
      <button class="update-product" data-product-id="${product.product_id}">Update Product</button>
    </div>
  `;
}
