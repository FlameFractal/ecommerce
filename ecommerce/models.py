from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True,
                             related_name='children')
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        if self.parent:
            return u'%s - %s' % (self.parent.name,
                                     self.name)
        return self.name

    @property
    def sorted_children(self):
        return self.children.order_by('name')
    

class Product(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField()
    size = models.TextField()
    photo = models.CharField(max_length=300)
    price_in_dollars = models.DecimalField(max_digits=4,
                                      decimal_places=2)
    categories = models.ManyToManyField(Category)
    stock = models.PositiveIntegerField(default=0)
    items_sold = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.slug)

    @property
    def unit_price_str(self):
        return "$%s" % self.price_in_dollars

    # photo = models.ImageField(upload_to='product_photo',
    #                         blank=True)


class Cart(models.Model):

    def add_product(self, product, quantity=1):
        items = CartItem.objects.filter(cart=self, product=product)
        if items.exists():
            cart_item = items[0]
            cart_item.quantity = cart_item.quantity + int(quantity)
            cart_item.save()
        else:
            cart_item = CartItem(cart=self, quantity=quantity, product=product)
            cart_item.save()
        return cart_item

    def update_quantity(self, cart_item_id, quantity):
        cart_item = self.items.get(pk=cart_item_id)
        if quantity == 0:
            cart_item.delete()
        else:
            if quantity <= cart_item.product.stock:
                cart_item.quantity = quantity
            else:
                cart_item.quantity = cart_item.product.stock
            cart_item.save()
        self.save()
        return cart_item

    def delete_item(self, cart_item_id):
        cart_item = self.items.get(pk=cart_item_id)
        cart_item.delete()
        self.save()

    def empty(self):
        if self.pk:
            self.items.all().delete()
            self.delete()

    @property
    def total_quantity(self):
        return sum([ci.quantity for ci in self.items.all()])

    @property
    def cart_total(self):
        return sum([ci.item_total for ci in self.items.all()])

    @property
    def cart_total_str(self):
        return "$%s" % sum([ci.item_total for ci in self.items.all()])

    @property
    def is_not_valid(self):
        for item in self.items.all():
            if not item.is_available:
                return item
        return False


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name="items")
    quantity = models.IntegerField()
    product = models.ForeignKey('Product')

    def __unicode__(self):
        return u'%s - %s' % (self.product.name, self.quantity)

    @property
    def item_total(self):
        return self.quantity * self.product.price_in_dollars

    @property
    def item_total_str(self):
        return "$%s" % (self.quantity * self.product.price_in_dollars)

    @property
    def is_available(self):
        return self.quantity <= self.product.stock


class Address(models.Model):
   # user = models.ForeignKey(User, blank=True, null=True, related_name="shipping_address")

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=20)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __unicode__(self):
        #return '%s %s (%s, %s)' % (self.first_name, self.last_name, self.zip_code, self.city)
        return self.as_text

    @property
    def as_text(self):
        return """
            First Name: %(first_name)s,
            Last Name: %(last_name)s,
            Address: %(address)s,
            Zip-Code: %(zipcode)s,
            City: %(city)s,
            State: %(state)s,
            Country: %(country)s
            """ % {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': '%s\n%s' % (self.address, self.address2),
            'zipcode': self.zip_code,
            'city': self.city,
            'state': self.state,
            'country': self.country,
        }


class Payment(models.Model):
    name_on_card = models.CharField(max_length=50)
    card_number = models.CharField(max_length=50)
    expiry_date = models.DateField()
    card_code =  models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s - %s' % (self.name_on_card, self.card_number)


class Order(models.Model):

    #SUBMITTED
    #PRELUAT
    #PROCESAT
    #LIVRARE
    #COMPLET

    PROCESSING = 1  # New order, addresses and shipping/payment methods chosen (user is in the shipping backend)
    CONFIRMING = 2 # The order is pending confirmation (user is on the confirm view)
    CONFIRMED = 3 # The order was confirmed (user is in the payment backend)
    COMPLETED = 4 # Payment backend successfully completed
    SHIPPED = 5 # The order was shipped to client
    CANCELLED = 6 # The order was cancelled

    STATUS_CODES = (
        (PROCESSING, 'Processing'),
        (CONFIRMING, 'Confirming'),
        (CONFIRMED, 'Confirmed'),
        (COMPLETED, 'Completed'),
        (SHIPPED, 'Shipped'),
        (CANCELLED, 'Cancelled'),
    )

    user = models.ForeignKey(User, blank=True, null=True, related_name="orders")
    address = models.ForeignKey(Address)
    payment = models.ForeignKey(Payment)
    order_total = models.PositiveIntegerField()
    status = models.PositiveIntegerField(choices=STATUS_CODES, default=PROCESSING)
    created_at = models.DateTimeField(auto_now_add = True)

    def add_item(self, product, quantity=1):
        order_item = OrderItem(order=self, quantity=quantity, product=product)
        order_item.save()
        product.stock = product.stock - quantity
        product.items_sold = product.items_sold + quantity
        product.save()

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.created_at)


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name="items")
    quantity = models.IntegerField()
    product = models.ForeignKey('Product')

    def __unicode__(self):
        return u'%s - %s' % (self.product.name, self.quantity)

    @property
    def item_total(self):
        return self.quantity * self.product.price_in_dollars

    @property
    def item_total_str(self):
        return "$%s" % (self.quantity * self.product.price_in_dollars)


class Advertisement(models.Model):
    owner = models.CharField(max_length=250)
    image = models.URLField()
    slogan = models.CharField(max_length=250)
    website = models.URLField()
    is_displayed = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return u'%s' % (self.owner)

# class ProductDetail(models.Model):
#     '''
#     The ``ProductDetail`` model represents information unique to a
#     specific product. This is a generic design that can be used
#     to extend the information contained in the ``Product`` model with
#     specific, extra details.
#     '''
#     product = models.ForeignKey('Product',
#                               related_name='details')
#     attribute = models.ForeignKey('ProductAttribute')
#     value = models.CharField(max_length=500)
#     description = models.TextField(blank=True)

#     def __unicode__(self):
#         return u'%s: %s - %s' % (self.product,
#                                  self.attribute,
#                                  self.value)

# class ProductAttribute(models.Model):
#     '''
#     The "ProductAttribute" model represents a class of feature found
#     across a set of products. It does not store any data values
#     related to the attribute, but only describes what kind of a
#     product feature we are trying to capture. Possible attributes
#     include things such as materials, colors, sizes, and many, many
#     more.
#     '''
#     name = models.CharField(max_length=300)
#     description = models.TextField(blank=True)

#     def __unicode__(self):
#         return u'%s' % self.name

