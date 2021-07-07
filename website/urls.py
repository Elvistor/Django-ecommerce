from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    path('', views.index, name="index"),
    path('acerca/', views.about, name="about"),
    path('productos/buscar-producto/', views.searchProduct, name="searchProduct"),
    path('productos/ver-producto/<int:product_id>', views.showProduct, name="showProduct"),
    path('productos/crear-producto/', views.createProduct, name="createProduct"),
    path('productos-categoria/<int:category_id>', views.categoryProducts, name="categoryProducts"),
    path('categorias/', views.indexCategory, name="indexCategory"),
    path('categorias/crear-categoria/', views.createCategory, name="createCategory"),
    path('categorias/editar-categoria/<int:category_id>', views.editCategory, name="editCategory"),
    path('categorias/eliminar-categoria/<int:category_id>', views.deleteCategory, name="deleteCategory"),
    path('productos/eliminar-producto/<int:producto_id>', views.deleteProduct, name="deleteProduct"),
    path('productos/editar-productos/<int:producto_id>', views.editProduct, name="editProduct"),
    path('productos/', views.indexProduct, name="indexProduct"),
    path('carrito/agregar', views.addCarrito, name="addCarrito"),
    path('carrito/ver', views.showCarrito, name="showCarrito"),
    path('carrito/eliminar-producto/<int:product_id>', views.deleteProductoCarrito, name="deleteProductoCarrito"),
    path('carrito/limpiar/', views.cleanCarrito, name="cleanCarrito"),
]