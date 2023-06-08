from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import User, Product, Purchase, PaymentCard, Message, Category, CategoryProduct, SupportTicket, Withdrawal, Contract
# from .forms import ProductForm, PurchaseForm, PaymentCardForm, MessageForm, SupportTicketForm, WithdrawalForm

def signup(request):
    if request.method == 'POST':
        # handle form submission
        # validate form data
        # create user object
        # send verification email
        # return success response
        return JsonResponse({'success': True})
    else:
        # display signup form
        return JsonResponse({'success': False, 'error': 'Method not allowed.'})

def enter_otp(request):
    if request.method == 'POST':
        # handle form submission
        # validate OTP
        # log user in
        # return success response
        return JsonResponse({'success': True})
    else:
        # display enter OTP form
        return JsonResponse({'success': False, 'error': 'Method not allowed.'})

@login_required
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    data = {
        'products': [{'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price, 'image_url': product.image.url} for product in products],
        'categories': [{'id': category.id, 'name': category.name} for category in categories],
    }
    return JsonResponse(data)

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = {
        'id': product.id,
        'title': product.title,
        'description': product.description,
        'price': product.price,
        'image_url': product.image.url,
        'user_id': product.user.id,
        'user_username': product.user.username,
    }
    return JsonResponse(data)

@login_required
def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    data = {
        'query': query,
        'products': [{'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price, 'image_url': product.image.url} for product in products],
    }
    return JsonResponse(data)

@login_required
def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()
    data = {
        'category_id': category.id,
        'category_name': category.name,
        'products': [{'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price, 'image_url': product.image.url} for product in products],
    }
    return JsonResponse(data)

@login_required
def messages(request):
    user = request.user
    messages = Message.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('-timestamp')
    data = {
        'messages': [{'id': message.id, 'sender_id': message.sender.id, 'sender_username': message.sender.username, 'recipient_id': message.recipient.id, 'recipient_username': message.recipient.username, 'text': message.text, 'timestamp': message.timestamp.isoformat()} for message in messages],
    }
    return JsonResponse(data)

@login_required
def chat(request, other_user_id):
    user = request.user
    other_user = get_object_or_404(User, pk=other_user_id)
    messages = Message.objects.filter(Q(sender=user, recipient=other_user) | Q(sender=other_user, recipient=user)).order_by('timestamp')
    data = {
        'other_user_id': other_user.id,
        'other_user_username': other_user.username,
        'messages': [{'id': message.id, 'sender_id': message.sender.id, 'sender_username': message.sender.username, 'recipient_id': message.recipient.id, 'recipient_username': message.recipient.username, 'text': message.text, 'timestamp': message.timestamp.isoformat()} for message in messages],
    }
    return JsonResponse(data)

@login_required
def support(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            send_mail(
                'New support ticket',
                'A new support ticket has been submitted. Please log in to the admin panel to view it.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.SUPPORT_EMAIL],
                fail_silently=True,
            )
            return JsonResponse({'success': True})
        else:
           return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SupportTicketForm()
        return JsonResponse({'success': False, 'html': form.as_p()})

@login_required
def withdrawals(request):
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user
            withdrawal.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = WithdrawalForm()
        return JsonResponse({'success': False, 'html': form.as_p()})

@login_required
def contracts(request):
    contracts = Contract.objects.filter(user=request.user)
    data = {
        'contracts': [{'id': contract.id, 'title': contract.title, 'description': contract.description, 'price': contract.price, 'status': contract.status} for contract in contracts],
    }
    return JsonResponse(data)