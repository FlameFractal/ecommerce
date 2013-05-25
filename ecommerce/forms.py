from django import forms
from django.forms.models import modelformset_factory
from models import CartItem, Address, Payment
from fields import CreditCardField, ExpiryDateField, VerificationValueField


class CartItemsForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=0, max_value=9999)

    class Meta:
        model = CartItem
        fields = ('quantity', )

    def save(self, *args, **kwargs):
        """
        We don't save the model using the regular way here because the
        Cart's ``update_quantity()`` method already takes care of deleting
        items from the cart when the quantity is set to 0.
        """
        quantity = self.cleaned_data['quantity']
        instance = self.instance.cart.update_quantity(self.instance.pk,
                quantity)
        return instance


class OrderAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('email', 'first_name', 'last_name', 'phone', 'address',
            'address2', 'city', 'zip_code', 'state', 'country')


class PaymentForm(forms.Form):
    name_on_card = forms.CharField(max_length=50, required=True)
    card_number = CreditCardField(required=True)
    expiry_date = ExpiryDateField(required=True)
    card_code = VerificationValueField(required=True)

    class Meta:
        model = Payment
        fields = ('name_on_card', 'card_number', 'expiry_date', 'card_code')

        
# def get_cart_item_formset(cart_items=None, data=None):
#     """
#     Returns a CartItemFormSet which can be used in the CartDetails view.

#     :param cart_items: The queryset to be used for this formset. This should
#       be the list of updated cart items of the current cart.
#     :param data: Optional POST data to be bound to this formset.
#     """
#     assert(cart_items is not None)
#     CartItemFormSet = modelformset_factory(CartItem, form=CartItemModelForm,
#             extra=0)
#     kwargs = {'queryset': cart_items, }
#     form_set = CartItemFormSet(data, **kwargs)

#     # The Django ModelFormSet pulls the item out of the database again and we
#     # would lose the updated line_subtotals
#     for form in form_set:
#         for cart_item in cart_items:
#             if form.instance.pk == cart_item.pk:
#                 form.instance = cart_item
#     return form_set