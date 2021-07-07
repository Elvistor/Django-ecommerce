from website.models import Categoria


#Pasar datos a todas las vistas
def data_templates(request):
    #Traemos todas las CAlegorías
    categorias = Categoria.objects.all()
    return { 
            "all_categories": categorias,
    } 