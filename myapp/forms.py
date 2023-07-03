from django import forms

class PaymentForm(forms.Form):
    account_type = forms.ChoiceField(choices=[('PayPal', 'PayPal'), ('Visa', 'Visa'), ('Payoneer', 'Payoneer'), ('Mastercard', 'Mastercard')])
    card_number = forms.CharField(max_length=16)
    expiration_date = forms.CharField(max_length=5)
    cvc = forms.CharField(max_length=3)
