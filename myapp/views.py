from django.http import JsonResponse
from django import forms
from .models import SupportTicket
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from myapp.models import User, Products, Purchase, Payment, Message, Categorys, Contract

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

def generate_otp_code():
    digits = "0123456789"
    otp_code = ""
    
    for _ in range(6):
        otp_code += random.choice(digits)
    
    return otp_code
from django.core.mail import send_mail

def send_otp_email(email, otp_code):
    subject = 'OTP Code'
    message = f'Your OTP code is: {otp_code}'
    sender_email = 'momo@gmail.com'
    recipient_email = email

    send_mail(subject, message, sender_email, [recipient_email])

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        user = request.user

        # Generate OTP code (you can customize the code generation logic)
        otp_code = generate_otp_code()

        # Save the OTP code to the database
        OTP.objects.create(user=user, otp_code=otp_code)

        # Send the OTP code to the user's email
        send_otp_email(user.email, otp_code)

        # Return success JSON response
        return JsonResponse({'success': True, 'message': 'OTP code sent to your email.'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def verify_otp(request):
    if request.method == 'POST':
        user = request.user
        otp_code = request.POST.get('otp_code')

        # Check if the OTP code is valid for the user
        otp = OTP.objects.filter(user=user, otp_code=otp_code).first()
        if otp is not None:
            # OTP code is valid, you can perform the account verification here

            # Delete the OTP code from the database
            otp.delete()

            # Return success JSON response
            return JsonResponse({'success': True, 'message': 'Account verified successfully.'})
        else:
            # Invalid OTP code
            return JsonResponse({'error': 'Invalid OTP code.'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


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







@login_required
def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.product_set.all()  # Access related products through the 'product_set' attribute

    data = {
        'category_id': category.id,
        'category_name': category.name,
        'products': [{'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price, 'image_url': product.image.url} for product in products],
    }

    return JsonResponse(data)


from django.shortcuts import get_object_or_404

@login_required
#http://127.0.0.1:8000/myapp/messages/?other_user=Mohamed@gmail.com
def messages(request): 
    # Get the current user's email
    user_email = request.user.email
    print(user_email)
    
    other_user_email = request.GET.get('other_user')
    print(other_user_email)

    # Get the user objects based on the email addresses
    user = User.objects.get(email=user_email)
    other_user = User.objects.get(email=other_user_email)

    # Fetch the messages between the current user and the other user
    messages = Message.objects.filter(
        Q(sender=user, recipient=other_user) | Q(sender=other_user, recipient=user)
    ).order_by('timestamp')

    # Prepare the data to be sent as a JSON response
    data = {
        'messages': [
            {
                'id': message.id,
                'sender_id': message.sender.id,
                'sender_username': message.sender.username,
                'recipient_id': message.recipient.id,
                'recipient_username': message.recipient.username,
                'text': message.text,
                'timestamp': message.timestamp.isoformat()
            } for message in messages
        ],
    }

    return JsonResponse(data)

@login_required
def chat(request):
    user_email = request.user.email
    other_user_email = request.GET.get('other_user')

    try:
        user = User.objects.get(email=user_email)
        other_user = User.objects.get(email=other_user_email)
    except User.DoesNotExist:
        return HttpResponse("User not found")

    messages = Message.objects.filter(
        Q(sender=user, recipient=other_user) | Q(sender=other_user, recipient=user)
    ).order_by('timestamp')

    data = {
        'other_user_id': other_user.id,
        'other_user_username': other_user.username if hasattr(other_user, 'username') else other_user_email,
        'messages': [
            {
                'id': message.id,
                'sender_id': message.sender.id,
                'sender_username': message.sender.username if hasattr(message.sender, 'username') else str(message.sender),
                'recipient_id': message.recipient.id,
                'recipient_username': message.recipient.username if hasattr(message.recipient, 'username') else str(message.recipient),
                'text': message.text,
                'timestamp': message.timestamp.isoformat()
            } for message in messages
        ],
    }

    return JsonResponse(data)

from django.contrib.auth.decorators import login_required

@login_required
def create_support_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST, request.FILES)
        if form.is_valid():
            support_ticket = form.save(commit=False)
            support_ticket.user = request.user
            support_ticket.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SupportTicketForm()
        return JsonResponse({'success': False, 'html': form.as_p()})


@login_required
def support_history(request):
    user = User.objects.get(email=request.user.email)
    support_tickets = SupportTicket.objects.filter(user=user) 
    data = {
        'support_tickets': []
    }

    if support_tickets.exists():
        data['support_tickets'] = [
            {
                'id': ticket.id,
                'subject': ticket.subject,
                'description': ticket.description,
                'status': ticket.status,
            }
            for ticket in support_tickets
        ]

    return JsonResponse(data)





@login_required
def contracts(request):
    user = User.objects.get(email=request.user.email)
    contracts = Contract.objects.filter(user=user)
    data = {
        'contracts': [{'id': contract.id, 'title': contract.title, 'description': contract.description, 'price': contract.price, 'status': contract.status} for contract in contracts],
    }
    return JsonResponse(data)
