document.addEventListener('DOMContentLoaded', () => {
  const sideMenu = document.getElementById('side-menu');
  const openMenu = document.getElementById('open-menu');
  const closeMenu = document.getElementById('close-menu');
  const categorySelect = document.getElementById('category-filter');
  const mobileCategorySelect = document.getElementById('category-filter-mobile');
  const productList = document.getElementById('product-list');

  // Open side menu on mobile
  openMenu.addEventListener('click', () => {
    sideMenu.classList.add('open');
  });

  // Close side menu on mobile
  closeMenu.addEventListener('click', () => {
    sideMenu.classList.remove('open');
  });

  // Shared fetch function
  function fetchFilteredProducts(category) {
    fetch('/filter-by-category', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category })
    })
    .then(res => res.json())
    .then(products => {
      productList.innerHTML = products.map(buildProductCard).join('');
    })
    .catch(err => console.error('Error fetching filtered products:', err));
  }

  // Build product card HTML
  function buildProductCard(product) {
    return `
      <div class="product-card">
        <h3>${product.category}</h3>
        <div class="product-details">
          <div class="product-info">
            <p>Sizes:</p>
            <div class="size-options">
              ${product.sizes.map(size => `<button class="size-option" data-size="${size}">${size}</button>`).join('')}
            </div>
            <p>Colors:</p>
            <div class="color-options">
              ${product.colors.map(color => `<button class="color-option" data-color="${color}">${color}</button>`).join('')}
            </div>
            <p>$${product.unit_price}</p>
          </div>
          <div class="product-image">
            <img src="${product.image_path[0]}" alt="Product Image" />
            <div class="view-images-button">
              <a href="/product-images/${product.product_id}">
                <button id="view-images">View Colors</button>
              </a>
            </div>
          </div>
        </div>
        <div class="card-footer">
          <button class="add-to-cart" data-product-id="${product.product_id}">Add to Cart</button>
        </div>
      </div>
    `;
  }

  // Filter handlers
  categorySelect?.addEventListener('change', () => {
    fetchFilteredProducts(categorySelect.value);
  });

  mobileCategorySelect?.addEventListener('change', () => {
    categorySelect.value = mobileCategorySelect.value;
    fetchFilteredProducts(mobileCategorySelect.value);
    sideMenu.classList.remove('open');
  });

  // Event delegation for cart logic and button selection
  productList.addEventListener('click', event => {
    const target = event.target;

    // Size selection
    if (target.classList.contains('size-option')) {
      const card = target.closest('.product-card');
      card.querySelectorAll('.size-option').forEach(btn => btn.classList.remove('selected'));
      target.classList.add('selected');
    }

    // Color selection
    if (target.classList.contains('color-option')) {
      const card = target.closest('.product-card');
      card.querySelectorAll('.color-option').forEach(btn => btn.classList.remove('selected'));
      target.classList.add('selected');
    }

    // Add to Cart
    if (target.classList.contains('add-to-cart')) {
      const card = target.closest('.product-card');
      const productId = target.getAttribute('data-product-id');
      const selectedSize = card.querySelector('.size-option.selected')?.dataset.size;
      const selectedColor = card.querySelector('.color-option.selected')?.dataset.color;

      if (!selectedSize || !selectedColor) {
        alert('Please select both size and color.');
        return;
      }

      fetch('/add-to-cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          product_id: productId,
          size: selectedSize,
          color: selectedColor
        })
      })
      .then(res => {
        if (res.ok) {
          alert('Added to cart!');
        } else {
          alert('Failed to add to cart.');
        }
      })
      .catch(err => {
        console.error('Add to cart error:', err);
        alert('Error adding to cart.');
      });
    }
  });
});
