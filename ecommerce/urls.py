from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns("",
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),

    url(r'^$', 'ecommerce.views.homepage', name='home'),
    url(r'^products$', 'ecommerce.views.products_all', name='products_all'),
    url(r'^category/(?P<slug>[-\w]+)$', 'ecommerce.views.products_for_category', name='products_for_category'),
    url(r'^product/(?P<slug>[-\w]+)$', 'ecommerce.views.product_details', name='product_details'),
    url(r'^search$', 'ecommerce.views.search', name='search'),
    url(r'^cart$', 'ecommerce.views.display_cart', name='display_cart'),
    url(r'^cart/add/(?P<product_id>\d+)$', 'ecommerce.views.add_to_cart', name='add_to_cart'),
    url(r'^checkout$', 'ecommerce.views.show_checkout', name='show_checkout'),
    url(r'^orders$', 'ecommerce.views.user_orders', name='user_orders'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
