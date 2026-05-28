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

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profiles:profile_settings")

    else:
        form = UserProfileForm(instance=user_profile, user=request.user)

    context = {
        "profile": user_profile,
        "active_enrollment": active_enrollment,
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

    enrollment_status = None

    next_class = None
    recent_attendance = Attendance.objects.none()

    if active_enrollment:
        enrollment_status = active_enrollment.status

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
        "enrollment_status": enrollment_status,
        "next_class": next_class,
        "recent_attendance": recent_attendance,
    }

    return render(request, "profiles/my_course.html", context)


@login_required
def my_attendance(request):
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

    recent_attendance = (
        Attendance.objects
        .filter(
            student=request.user,
            class_session__course=active_enrollment.course,
            status="attended",
        )
        .select_related(
            "class_session",
            "class_session__course",
        )
        .order_by("-class_session__start_time")
    )
    
    class_session = (
       Attendance.objects
       .filter(
           
       ) 
    )

    context = {
        "profile": profile,
        "active_enrollment": active_enrollment,
        "recent_attendance": recent_attendance,
    }

    return render(request, "profiles/my_attendance.html", context)