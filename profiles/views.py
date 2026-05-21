from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import UserProfile
from .forms import UserProfileForm

from courses.models import CourseEnrollment, ClassSession, Attendance

@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    active_enrollment = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
            status="active"
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
        .first()
    )

    next_class = None

    if active_enrollment:
        next_class = (
            ClassSession.objects
            .filter(
                course=active_enrollment.course,
                is_cancelled=False,
                start_time__gte=timezone.now()
            )
            .order_by("start_time")
            .first()
        )

    context = {
        "profile": user_profile,
        "active_enrollment": active_enrollment,
        "next_class": next_class,
    }

    return render(request, "profiles/profile.html", context)


@login_required
def profile_settings(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profiles:profile_settings")
    else:
        form = UserProfileForm(instance=profile, user=request.user)

    context = {
        "profile": profile,
        "form": form,
    }

    return render(request, "profiles/profile_settings.html", context)


@login_required
def my_course(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    active_enrollment = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
            status="active"
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
        .first()
    )

    next_class = None
    recent_attendance = Attendance.objects.none()

    if active_enrollment:
        next_class = (
            ClassSession.objects
            .filter(
                course=active_enrollment.course,
                is_cancelled=False,
                start_time__gte=timezone.now()
            )
            .order_by("start_time")
            .first()
        )

        recent_attendance = (
            Attendance.objects
            .filter(
                student=request.user,
                class_session__course=active_enrollment.course,
            )
            .select_related("class_session")
            .order_by("-class_session__start_time")[:5]
        )

    context = {
        "profile": profile,
        "active_enrollment": active_enrollment,
        "next_class": next_class,
        "recent_attendance": recent_attendance,
    }

    return render(request, "profiles/my_course.html", context)

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
