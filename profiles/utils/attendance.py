def build_enrollment_attendance_summary(enrollment):
    attendance_submitted_classes = enrollment.complete_attendance_submitted_classes

    return {
        "attended_count": enrollment.classes_attended,
        "missed_count": enrollment.classes_missed,
        "excused_count": enrollment.classes_excused,
        "total_attendance_records": attendance_submitted_classes,
        "attendance_submitted_classes": attendance_submitted_classes,
        "attendance_percentage": enrollment.attendance_percentage,
    }