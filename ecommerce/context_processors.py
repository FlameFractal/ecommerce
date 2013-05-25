from models import Category, Product, Advertisement

def menu_categories(request):
    return {'menu_categories': Category.objects.filter(parent__isnull=True).order_by('name')}

def top_products(request):
    return {'top_products': Product.objects.all().order_by('-items_sold')[:4]}

def advertisements(request):
    return {'advertisements': Advertisement.objects.filter(is_displayed=True).order_by('position')}