from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from models import Product, Cart, CartItem, Payment, Address, Order, Category
from forms import CartItemsForm, OrderAddressForm, PaymentForm
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User

def _get_referer_view(request, default=None):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return default
    referer = re.sub('^https?:\/\/', '', referer).split('/')
    referer = u'/' + u'/'.join(referer[1:])
    return referer

def _get_cart_from_session(request):
    session_cart = None
    session = getattr(request, 'session', None)
    if session is not None:
        cart_id = session.get('cart_id')
        if cart_id:
            try:
                session_cart = Cart.objects.get(pk=cart_id)
            except Cart.DoesNotExist:
                session_cart = None
    return session_cart

def _get_or_create_cart(request):
    cart = None
    if not hasattr(request, 'cart_object'):
        cart = _get_cart_from_session(request)
        if not cart and getattr(request, 'session', None) is not None:
            cart = Cart()
        if not cart.pk:
            cart.save()
            request.session['cart_id'] = cart.pk
        request.session['cart_object'] = cart
    cart = request.session['cart_object']
    return cart


def homepage(request):
    product_list = Product.objects.all().order_by('?')[:18]
    return render_to_response("homepage.html",
                              {'product_list': product_list},
                              context_instance=RequestContext(request))


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render_to_response("product.html", 
                             {'product': product}, 
                             context_instance=RequestContext(request))


def products_for_category(request, slug):
    categories = []
    category = Category.objects.get(slug=slug)
    categories.append(category)
    categories.extend(category.children.all())
    product_list = Product.objects.filter(categories__in=categories).distinct()
    return render_product_list(request, product_list)


def products_all(request):
    product_list = Product.objects.all()
    return render_product_list(request, product_list)


def render_product_list(request, product_list, criteria=None):
    paginator = Paginator(product_list, 8)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render_to_response("product_list.html", 
                             {'product_list': products,
                              'criteria': criteria }, 
                             context_instance=RequestContext(request))


def display_cart(request):
    try: 
        cart_items = request.session['cart_object'].items.all()
    except KeyError:
        cart_items = []

    try:
        invalid_item = request.session['invalid_item']
    except KeyError:
        invalid_item = None

    if invalid_item:
        del request.session['invalid_item']

    CartItemsFormSet = modelformset_factory(CartItem, form = CartItemsForm, extra=0, can_delete=True)
    if cart_items:
        formset = CartItemsFormSet(queryset = cart_items)
    else:
        formset = None
    if request.method == 'POST':
        formset = CartItemsFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            # update formset in case the above save removed any items
            try: 
                cart_items = request.session['cart_object'].items.all()
            except KeyError:
                cart_items = []
            formset = CartItemsFormSet(queryset = cart_items)

    # TODO: if there are no more items redirect?
    return render_to_response("cart.html", 
                             {'formset': formset,
                              'invalid_item': invalid_item},
                             context_instance=RequestContext(request))


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request)
    cart.add_product(product)
    ref = _get_referer_view(request, 'homepage.html')
    return HttpResponseRedirect(ref)

def show_checkout(request):

    try:
        cart = request.session['cart_object']
    except KeyError:
        return redirect('products_all')

    invalid_item = cart.is_not_valid
    if invalid_item:
        request.session['invalid_item'] = invalid_item
        return redirect('display_cart')

    address_form = OrderAddressForm()
    payment_form = PaymentForm()

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        address_form = OrderAddressForm(request.POST)

        if payment_form.is_valid() and address_form.is_valid():
            payment_data = payment_form.cleaned_data
            address_data = address_form.cleaned_data

            payment = Payment(name_on_card=str(payment_data['name_on_card']),
                              card_number=str(payment_data['card_number']),
                              expiry_date=payment_data['expiry_date'],
                              card_code=str(payment_data['card_code']))
            payment.save()

            address = Address(first_name=str(address_data['first_name']),
                              last_name=str(address_data['last_name']),
                              email=str(address_data['email']),
                              phone=str(address_data['phone']),
                              address=str(address_data['address']),
                              address2=str(address_data['address2']),
                              city=str(address_data['city']),
                              zip_code=str(address_data['zip_code']),
                              state=str(address_data['state']),
                              country=str(address_data['country']))
            address.save()

            try:
                user = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                user = None
            
            order = Order(user=user, address=address, payment=payment, order_total=cart.cart_total)
            order.save()

            for item in cart.items.all():
                order.add_item(product=item.product, quantity=item.quantity)
                item.delete()
            cart.delete()

            del request.session['cart_object']
            del request.session['cart_id']

            return redirect('user_orders')

    return render_to_response("checkout_address.html", 
                             {'address_form': address_form,
                              'payment_form': payment_form},
                             context_instance=RequestContext(request))

def search(request):
    query = request.GET['q']
    product_list = Product.objects.filter(name__contains=query)
    return render_product_list(request, product_list, criteria=query)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user__id=user_id).order_by('-created_at')

    # import pdb
    # pdb.set_trace()

    return render_to_response("order_list.html", 
                             {'orders': orders},
                             context_instance=RequestContext(request))
