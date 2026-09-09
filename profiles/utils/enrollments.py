from django.db.models import Case, When, Value, IntegerField, F, DateField


def order_enrollments_by_course_status(queryset):
    return (
        queryset
        .annotate(
            status_order=Case(
                When(course__status="active", then=Value(1)),
                When(course__status="confirmed", then=Value(2)),
                When(course__status="paused", then=Value(3)),
                When(course__status="completed", then=Value(4)),
                When(course__status="cancelled", then=Value(5)),
                default=Value(99),
                output_field=IntegerField(),
            ),
            completed_date_order=Case(
                When(
                    course__status="completed",
                    then=F("course__end_date"),
                ),
                default=Value(None),
                output_field=DateField(),
            ),
        )
        .order_by(
            "status_order",
            "course__name",
            "-completed_date_order",
        )
    )