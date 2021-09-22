from django.shortcuts import render
from django.views.generic import ListView, DetailView
from App_Shop.models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.


def home(request):
    category = request.GET.get('category')

    if category == None:
        products = Product.objects.order_by('-created')
    else:
        products = Product.objects.filter(category__name=category)


    categories = Category.objects.all()

        # for paging the home page

    page_num = request.GET.get('page')
    paginator = Paginator(products, 12)

    try:
        products= paginator.page(page_num)
    except  PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'App_Shop/home.html', context)

class  ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'App_shop/product_detail.html'

def search_items(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        items = Product.objects.filter(name__contains = searched)
        return render(request, 'App_Shop/search.html', {'searched':searched, 'items':items})
    else:
        return render(request, 'App_Shop/search.html', context={})
