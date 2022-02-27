from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import json
import shop.bd_form
import shop.price_form


def about(request):
    return render(request, 'shop/about.html')


def contacts(request):
    return render(request, 'shop/contacts.html')


def get_base():
    """Function get data from base.txt"""
    with open('Price/base.txt') as fh:
        base = json.load(fh)
    return base


def data_refresh(base: dict):
    """Function create instances of Category and Product from base"""
    for key, val in base.items():
        try:
            Category.objects.get(name=key)
            print(f'"{key}" - category exists!')
        except:
            Category(name=key).save()
            print(f'"{key}" - category created!')
        finally:
            for equip, desc in val.items():
                try:
                    inst = Product.objects.get(name=equip)
                    inst.price = desc[1]
                    inst.stock = desc[2]
                    inst.save()
                    print(f'Stock balance and price for {equip} updated.')
                except:
                    cat = Category.objects.get(name=key)
                    if len(desc) == 5:
                        Product(category=cat, name=equip, product_name=desc[0],
                                price=desc[1], stock=desc[2]).save()
                        print(f'{equip} product card created ')
                    else:
                        if len(desc[6]) == 0:
                            Product(category=cat, name=equip, product_name=desc[0], description=desc[5],
                                    price=desc[1], stock=desc[2]).save()
                            print(f'{equip} product card created ')
                        else:
                            Product(category=cat, name=equip, product_name=desc[0], image=desc[6][0],
                                    description=desc[5], price=desc[1], stock=desc[2]).save()
                            print(f'{equip} product card created ')


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 15)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        products = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        products = paginator.page(paginator.num_pages)
    return render(request, 'shop/product/list.html',
                  {'page': page,
                   'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


def run():
    shop.price_form.directory_cleaning()
    outfilename = shop.price_form.file_download("https://microinform.by/downloads/m_price.rar")
    shop.price_form.rar_unpacking(outfilename)
    data_dict = shop.price_form.price_conversion(percent=50)
    shop.price_form.price_create(data_dict)
    base_for_save = shop.bd_form.dict_convert(shop.bd_form.add_data(data_dict))
    shop.bd_form.save_base(base_for_save)
    data_refresh(base_for_save)

# run()


def search(request):
    query = request.GET.get('q')
    search_list = Product.objects.filter(Q(name__icontains=query) | Q(product_name__icontains=query), available=True)
    return render(request, 'shop/search_results.html',
                  {'products': search_list})
