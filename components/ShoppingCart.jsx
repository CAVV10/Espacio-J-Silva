import '../styles/ShoppingCart.css';

return (
  <div>
    <h2>Carrito de Compras</h2>
    
    {products.length > 0 ? (
      <div className="cart-table">
        <div className="cart-header">
          <div>Producto</div>
          <div>Precio</div>
          <div>Cantidad</div>
          <div>Subtotal</div>
          <div>Acciones</div>
        </div>
        {/* ... resto del código de los productos ... */}
      </div>
    ) : (
      <div className="empty-cart">
        <div className="cart-icon">🛒</div>
        <h3>Tu carrito está vacío</h3>
        <p>Agrega productos para comenzar tu compra</p>
        <button className="catalog-button">
          <span className="catalog-icon">📋</span>
          Ir al catálogo
        </button>
      </div>
    )}
  </div>
); 