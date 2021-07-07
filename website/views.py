from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
#Impartamos Q para filtrar en la busqueda
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
#Para los mensajes
from django.contrib import messages

from .models import Categoria, Producto, Carrito
from .forms import *

#Creamos un decorador para verificar el grupo
def group_required(*group_names):
    """ Grupos, verificar si pertenece a grupo """
    def check(user):
        if user.groups.filter(name__in=group_names).exists() | user.is_superuser:
            return True
        else:
            return False
    # Si no se pertenece al grupo, redirigir a /accounts/forbidden
    return user_passes_test(check, '/accounts/forbidden')

# Create your views here.
#Vista Principal
def index(request):
    #Buscamos todos lo productos y traesmos los 10 primeros
    productsTopTen = Producto.objects.all()[:9]
    #Buscamos todos lo productos y traesmos los que siguen a los primeros 10
    productsLastTen = Producto.objects.all()[9:]
    return render(request, ['ecommerce/index.html'],{
        'productsTopTen':productsTopTen,
        'productsLastTen':productsLastTen,
    })

#Vista Acerca de 
def about(request):
    return render(request, 'ecommerce/about.html')

#Vista Busqueda de Productos
def searchProduct(request):
    #Recibimos los datos a buscar
    search = request.GET.get("search")
    #Buscamos todos lo productos
    productos = Producto.objects.all()
    #Comprobamos que tengamos productos y que tengamos algo en search
    if productos and search:
        #Filtramos los productos
        productos = productos.filter(
            #Buscamos en el titulo
            Q(titulo__icontains = search) |
            #O buscamos en la descripcion
            Q(descripcion__icontains = search)
        ).distinct()#para evitar los repetidos en el filtro
        return render(request, 'ecommerce/productos/search_products.html',{
            'itemSearch': search,
            "productos": productos
        })
    else:
        return redirect(reverse("website:index"))

#Vista Ver un Producto
def showProduct(request, product_id):
    #Buscamos el producto por el id
    producto = get_object_or_404(Producto, id=product_id)
    return render(request, "ecommerce/productos/show_product.html",{
        'producto': producto
    })

#Vista Filtro por Categorías
def categoryProducts(request, category_id):
    #Buscamos la categoria por el id
    categoria = get_object_or_404(Categoria, id=category_id)
    #Buscamos todos lo productos
    productos = Producto.objects.all()
    #Filtramos los productos
    productos = productos.filter(categoria=categoria).distinct()
    return render(request,"ecommerce/productos/search_products.html", {
    "productos": productos,
    "itemSearch": categoria
    })

################### Administración de Carrito ################################
@login_required()
def addCarrito(request):
    if request.method == 'POST':
        product_id = int(request.POST.get("product_id"))
        producto = get_object_or_404(Producto, id=product_id)
        usuario = User.objects.get(username=request.user)
        #Comprobamos si tiene un carrito sino lo creamos
        try:
            carrito = Carrito.objects.get(usuario=usuario)
        except:
            carrito = Carrito.objects.create(usuario=usuario)

        carrito.listaProductos.add(producto)
        carrito.save()
        #Mensajes
        messages.add_message(request, messages.SUCCESS, 'El Producto se Agrego a tu Carrito.')    
        return HttpResponseRedirect(reverse("website:index"))
    else:
        return HttpResponseRedirect(reverse("website:index"))

@login_required()
def showCarrito(request):
    #Obtenemos el usuario
    usuario = User.objects.get(username=request.user)
    #Comprobamos si tiene un carrito sino lo creamos
    try:
        carrito = Carrito.objects.get(usuario=usuario)
        productos = carrito.listaProductos.all()
        return render(request, 'ecommerce/carrito/index.html', {
        'carrito': carrito,
        'productos':productos
        })
    except:
        messages.add_message(request, messages.SUCCESS, 'No Tienes Productos en Tu carrito.')
        return HttpResponseRedirect(reverse("website:index"))

@login_required()
def deleteProductoCarrito(request, product_id):
    #Obtenemos el Producto
    producto = get_object_or_404(Producto, id=product_id)
    #Buscamos el usuario
    usuario = User.objects.get(username=request.user)
    #Buscamos el carrito
    carrito = Carrito.objects.get(usuario=usuario)
    #Removemos el producto
    carrito.listaProductos.remove(producto)
    print(carrito)
    #Mensajes
    messages.add_message(request, messages.SUCCESS, 'El producto se ha quitado de su carrito')
    return HttpResponseRedirect(reverse("website:showCarrito"))

@login_required()
def cleanCarrito(request):
    if request.method == 'POST':
        usuario = User.objects.get(username=request.user)
        #Comprobamos si tiene un carrito sino lo creamos
        try:
            carrito = get_object_or_404(Carrito, usuario=usuario)
            carrito.delete()
            #Mensajes
            messages.add_message(request, messages.SUCCESS, 'Tu Carrito se Limpio Correctamente.') 
            return HttpResponseRedirect(reverse("website:index"))   
        except:   
            #Mensajes
            messages.add_message(request, messages.SUCCESS, 'Tu Carrito se Limpio Correctamente.') 
            return HttpResponseRedirect(reverse("website:index"))   
    else:
        return HttpResponseRedirect(reverse("website:index"))

################ Administración de Categorías ##############################
@group_required('Moderador')
def indexCategory(request):
    #Traemos todas las categorias para poder mostrarlas 
    categorias = Categoria.objects.all()
    return render(request,"ecommerce/categoria/index.html",{'categorias':categorias})
    
@group_required('Moderador')
def createCategory(request):
    if request.method == "POST":
        form = FormCategoria(data=request.POST)
        if form.is_valid():
            form.save()
            #Mensajes
            messages.add_message(request, messages.SUCCESS, 'Categoria Creada Correctamente.')
            return HttpResponseRedirect(reverse("website:indexCategory"))
    else:
        #Generamos el formulario
        form = FormCategoria()
        return render(request,"ecommerce/categoria/create_category.html",{
            'form' : form
            })

@group_required('Moderador')
def editCategory(request,category_id):
    #Buscamos la categoria
    categoria = get_object_or_404(Categoria, id=category_id)
    if request.method == "POST":
        form = FormCategoria(data=request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            #Mensajes
            messages.add_message(request, messages.SUCCESS, 'La edición se ha editaco con éxito Correctamente.')
            return HttpResponseRedirect(reverse("website:indexCategory"))
    else:
        #Generamos el formulario
        form = FormCategoria(instance = categoria)
        return render(request,"ecommerce/categoria/edit_category.html",{
            'categoria':categoria,
            'form' : form
            })

@group_required('Moderador')
def deleteCategory(request, category_id):
    #Buscamos la categoria
    categoria = get_object_or_404(Categoria, id=category_id)
    categoria.delete()
    #Mensajes
    messages.add_message(request, messages.SUCCESS, 'La Categoria se eliminó Correctamente.')
    return HttpResponseRedirect(reverse("website:indexCategory"))

################ Administración de Productos ##############################
@group_required('Moderador')
def indexProduct(request):
    #Traemos todas los productos para poder mostrarlas 
    productos = Producto.objects.all()
    return render(request,"ecommerce/productos/index.html",{'productos':productos})

@group_required('Moderador')
def deleteProduct(request, producto_id):
    #Buscamos el producto
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    #Mensajes
    messages.add_message(request, messages.SUCCESS, 'El producto se ha eliminado')
    return redirect("website:indexProduct")

@group_required('Moderador')
def editProduct(request, producto_id):
    #Buscamos el producto
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        if request.FILES:
            form = FormProducto(data=request.POST, files=request.FILES, instance=producto)
        else:
            form = FormProducto(data=request.POST, instance=producto)
        if form.is_valid():
            form.save()
            #Mensajes
            messages.add_message(request, messages.SUCCESS, 'El Producto se ha modificado Correctamente.')
            return HttpResponseRedirect(reverse("website:indexProduct"))

    else:
        #Generamos el formulario
        form = FormProducto(instance = producto)
        return render(request,"ecommerce/productos/edit_product.html",{
            'producto':producto,
            'form' : form
            })

#Vista Alta Producto comprobamos que pertenece al grupo Moderador
@group_required('Moderador')
def createProduct(request):
    if request.method == 'POST':
        form = FormProducto(data=request.POST, files=request.FILES, instance=Producto(imagen=request.FILES['imagen']))
        if form.is_valid():
            form.save()     
            #Mensajes
            messages.add_message(request, messages.SUCCESS, 'El Producto se ha Correctamente.')
            return HttpResponseRedirect(reverse("website:indexProduct"))
    else:
        form = FormProducto()
        return render(request, 'ecommerce/productos/create_product.html', {
        'form': form
        })
