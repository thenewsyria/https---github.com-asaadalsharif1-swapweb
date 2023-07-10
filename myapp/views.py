from django.http import JsonResponse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from myapp.models import User, Products,Favorit, Purchase, Payment, Message, Categorys, Contract

from django.core.mail import send_mail
from .models import OTP

from django.core.exceptions import ValidationError



@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            full_name = request.POST['full_name']
            email = request.POST['email']
            password = request.POST['password']
            phone_number = request.POST['phone_number']
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {e}'}, status=400)

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists.'}, status=400)

        # Create the user
        user = User(email=email)
        user.full_name = full_name
        user.phone_number = phone_number
        user.set_password(password)
        user.save()

        # Return success JSON response
        return JsonResponse({'success': True, 'user_email': user.email})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

from django.contrib.auth import authenticate, login


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {e}'}, status=400)

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'user_email': user.email})
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

import random
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        # Get the currently logged-in user
        user = request.user

        # Generate a random OTP code
        otp_code = str(random.randint(100000, 999999))

        # Save the OTP code to the database
        otp = OTP(user=user, otp_code=otp_code)
        otp.save()

        # Send the OTP code to the user via email
        subject = 'OTP Code'
        message = f'Your OTP code is: {otp_code}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email

        try:
            send_mail(subject, message, from_email, [to_email])
            return JsonResponse({'success': True, 'message': 'OTP sent successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.contrib.auth import login
from django.http import JsonResponse
from social_django.utils import psa
@csrf_exempt
@psa('social:complete')
def social_login(request, backend):
    user = request.backend.do_auth(request.GET.get('access_token'))
    if user:
        login(request, user)
        return JsonResponse({'status': 'success', 'message': 'Logged in successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Failed to authenticate.'})
@psa('social:complete')

@csrf_exempt
def social_sign_up(request, backend):
    user = request.backend.do_auth(request.GET.get('access_token'))
    if user:
        user.is_active = True  # Activate the user
        user.save()
        login(request, user)
        return JsonResponse({'status': 'success', 'message': 'Signed up and logged in successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Failed to authenticate or sign up.'})


def get_categories(request):
    categories = Categorys.objects.all()
    data = {
        'categories': [
            {
                'id': category.id,
                'name': category.name,
                'image': category.image.url
            }
            for category in categories
        ]
    }
    return JsonResponse(data)

def get_products(request):
    user_email = request.user.email
    user=User.objects.get(email=user_email)
    print(user)
    products = Products.objects.filter(user=user)
    data = {
        'products': [
            {
                'id': product.id,
                'title': product.title,
                'price': str(product.price),
                'description': product.description,
                'image': product.image.url,
                'video': product.video.url,
                'category': {
                    'id': product.category.id,
                    'name': product.category.name
                }
            }
            for product in products
        ]
    }
    return JsonResponse(data)
@csrf_exempt
def addProductToFavorit(request, product_id):
    user_email = request.user.email
    user = User.objects.get(email=user_email)
    product = Products.objects.get(id=product_id)

    favorit = Favorit(user=user, product=product)
    favorit.save()

    data = {
        'message': 'Product added to favorites successfully.',
    }
    return JsonResponse(data)

from django.db.models import Q

def search_products(request):
    query = request.GET.get('query')  # Get the search query from the request parameters
    
    if query:
        products = Products.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        
        data = {
            'products': [
                {
                    'id': product.id,
                    'title': product.title,
                    'price': str(product.price),
                    'description': product.description,
                    'image': product.image.url,
                    'video': product.video.url,
                    'category': {
                        'id': product.category.id,
                        'name': product.category.name
                    }
                }
                for product in products
            ]
        }
        
        return JsonResponse(data)
    
    return JsonResponse({'message': 'No search query provided'})


from .models import Support
@csrf_exempt
def submit_support(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        support = Support(subject=subject, description=description, image=image)
        support.save()

        return JsonResponse({'message': 'Support ticket submitted successfully'})

    return JsonResponse({'message': 'Invalid request method'})

from .models import Support

def historysupport(request):
    supports = Support.objects.all()
    data = {
        'supports': [
            {
                'id': support.id,
                'subject': support.subject,
                'description': support.description,
                'status': support.status,
            }
            for support in supports
        ]
    }
    return JsonResponse(data)

from django.shortcuts import get_object_or_404
from .models import Support, Message
@csrf_exempt
def live_support(request, support_id):
    support = get_object_or_404(Support, id=support_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        # Create a new message associated with the support ticket
        message = Message(content=content, support=support)
        message.save()

        # Add your code to handle the message and communicate with the support team
        # You can send notifications to the support team or update the status of the support ticket based on the message content

        return JsonResponse({'message': 'Message sent successfully'})

    elif request.method == 'GET':
        # Retrieve all the messages associated with the support ticket
        messages = support.messages.all()
        
        data = {
            'support_id': support.id,
            'subject': support.subject,
            'description': support.description,
            'status': support.status,
            'messages': [
                {
                    'id': message.id,
                    'content': message.content,
                    'timestamp': message.timestamp,
                    'sender': message.sender.email
                }
                for message in messages
            ]
        }

        return JsonResponse(data)

    return JsonResponse({'message': 'Invalid request method'})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def payment_gateway(request):
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        card_type = request.POST.get('card_type')
        card_number = request.POST.get('card_number')
        expiration_date = request.POST.get('expiration_date')
        cvc = request.POST.get('cvc')

        if user is not None:
            # Create the payment card
            payment_card = Payment(user=user, card_type=card_type, card_number=card_number, expiration_date=expiration_date, cvc=cvc)
            payment_card.save()

            # Return success JSON response
            return JsonResponse({'success': True, 'message': 'Payment card added successfully'})
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

## after this line I am not sure


@csrf_exempt
def chat(request, product_id):
    product = Products.objects.get(id=product_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        sender = request.user
        receiver = product.user

        # Create a new message
        message = Message.objects.create(sender=sender, receiver=receiver, product=product, content=content)

        # Return success JSON response
        return JsonResponse({'success': True, 'message': 'Message sent successfully.'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def get_messages(request, product_id):
    product = Products.objects.get(id=product_id)
    sender = request.user
    receiver = product.user

    # Retrieve all messages between the sender and receiver for the given product
    messages = Message.objects.filter(sender__in=[sender, receiver], receiver__in=[sender, receiver], product=product).order_by('created_at')

    data = {
        'messages': [
            {
                'sender': message.sender.email,
                'receiver': message.receiver.email,
                'content': message.content,
                'created_at': message.created_at
            }
            for message in messages
        ]
    }
    return JsonResponse(data)

@login_required
def contracts(request):
    user = User.objects.get(email=request.user.email)
    contracts = Contract.objects.filter(user=user)
    data = {
        'contracts': [{'id': contract.id, 'title': contract.title, 'description': contract.description, 'price': contract.price, 'status': contract.status} for contract in contracts],
    }
    return JsonResponse(data)
