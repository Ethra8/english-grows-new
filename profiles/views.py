from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm
# from checkout.models import Order


# ---------------------------
# PROFILE LANDING PAGE
# ---------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            instance=user_profile,
            user=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Update failed. Please check the form.')
    else:
        form = UserProfileForm(
            instance=user_profile,
            user=request.user
        )

    return render(request, 'profiles/profile.html', {
        'profile': user_profile,
        'form': form,
    })
# ---------------------------
# ACCOUNT INFORMATION PAGE
# ---------------------------
# @login_required
# def account_information(request):
#     profile = get_object_or_404(UserProfile, user=request.user)

#     if request.method == 'POST':
#         print("POST DATA:", request.POST)
#         form = UserProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully')
#             return redirect('profile')  # IMPORTANT
#         else:
#             messages.error(request, 'Update failed. Please ensure the form is valid.')
#     else:
#         form = UserProfileForm(instance=profile)

#     return render(request, 'profiles/profile.html', {
#         'profile': profile,
#         'form': form,
#     })


# ---------------------------
# ORDER HISTORY PAGE
# ---------------------------
# @login_required
# def order_history(request):
#     profile = get_object_or_404(UserProfile, user=request.user)
#     orders = Order.objects.filter(user_profile=profile).order_by('-date')

#     return render(request, 'profiles/order_history.html', {
#         'profile': profile,
#         'orders': orders,
#     })


# ---------------------------
# SINGLE ORDER DETAIL
# ---------------------------
# @login_required
# def order_detail(request, order_number):
#     profile = get_object_or_404(UserProfile, user=request.user)
#     order = get_object_or_404(Order, order_number=order_number)

#     messages.info(request, f'This is a past confirmation for order {order_number}. '
#                            'A confirmation email was sent on the order date.')

#     return render(request, 'checkout/checkout_success.html', {
#         'order': order,
#         'from_profile': True,
#     })# Create your views here.
