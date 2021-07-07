from django.db.models import Sum
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    descripcion = models.CharField(max_length=64, null=False)

    def __str__(self):
        return f"{self.descripcion}"

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, related_name="clasificacion_categorias", null=True, blank=True)
    titulo = models.CharField(max_length=250, null=False)
    descripcion = models.CharField(max_length=2000, null=False)
    #Instalar Pillow para poder usarlo
    imagen = models.FileField(upload_to='imgproducts/')
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    #Para obtener los datos de cuando se creo y cuando se modifico
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.categoria} - {self.titulo}"

    #Metadata
    class Meta:
        #Order por el mas reciente
        ordering = ["-created_at"]

#Un carrito por usuario
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="usuario")
    listaProductos = models.ManyToManyField(Producto)
    total_carrito = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)

    #Para obtener los datos de cuando se creo y cuando se modifico
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    """
        Opciones de propiedad calculada o computada
    """
    # Opción 1
    def _get_total_carrito(self):
        return sum([carrito.precio for carrito in self.listaProductos.all()])
    total_carrito = property(_get_total_carrito)

    def __str__(self):
        return f"{self.usuario} - ${self.total_carrito}"

