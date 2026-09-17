def build_enrollment_attendance_summary(enrollment):
    metrics = enrollment.attendance_metrics

    return {
        "attended_count": metrics["attended_classes"],
        "missed_count": metrics["missed_classes"],
        "excused_count": metrics["excused_classes"],
        "total_attendance_records": metrics["total_submitted_attendance_records"],
        "attendance_submitted_classes": enrollment.complete_attendance_submitted_classes,
        "attendance_percentage": metrics["attendance_percentage"],
    }