from .models import Yacht, Rental
from django.shortcuts import render, get_object_or_404, redirect
from .forms import RentalForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def yacht_list(request):
    yachts = Yacht.objects.all()
    context = {
        'yachts': yachts
    }
    return render(request, 'rentals/yacht_list.html', context)

def yacht_detail(request, pk):
    yacht = get_object_or_404(Yacht, pk=pk)
    context = {
        'yacht': yacht,
    }
    return render(request, 'rentals/yacht_detail.html', context)


@login_required
def rental_form(request, pk):
    yacht = get_object_or_404(Yacht, pk=pk)

    initial_data = {
        'name': request.user.first_name,
        'surname': request.user.last_name,
    }

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.yacht = yacht
            rental.user = request.user
            rental.total_price = yacht.price_per_day * (
                (rental.end_date - rental.start_date).days or 1
            )
            rental.save()
            return redirect('my_rentals')
    else:
        form = RentalForm(initial=initial_data)

    context = {
        'yacht': yacht,
        'form': form,
    }
    return render(request, 'rentals/rental_form.html', context)


@login_required
def my_rentals(request):
    rentals = Rental.objects.filter(user=request.user)
    context = {
        'rentals': rentals,
    }
    return render(request, 'rentals/my_rentals.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Yacht Rental Account'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, message)
            return render(request, 'registration/registration_complete.html')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('yacht_list')
    else:
        return HttpResponse('Activation link is invalid!', status=400)

def custom_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('yacht_list')

from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def profile(request):
    reservations = Rental.objects.filter(user=request.user)
    return render(request, 'rentals/profile.html', {'reservations': reservations})

def rent_options(request, pk):
    yacht = get_object_or_404(Yacht, pk=pk)
    return render(request, 'rentals/rent_options.html', {'yacht': yacht})


@login_required
def edit_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)

    if request.method == 'POST':
        form = RentalForm(request.POST, instance=rental)
        if form.is_valid():
            form.save()
            return redirect('my_rentals')
    else:
        form = RentalForm(instance=rental)

    return render(request, 'rentals/rental_form.html', {'form': form, 'rental': rental})