
def build_enrollment_attendance_summary(enrollment):
    return {
        "attended_count": enrollment.classes_attended,
        "missed_count": enrollment.classes_missed,
        "excused_count": enrollment.classes_excused,
        "total_attendance_records": enrollment.total_completed_classes,
        "attendance_percentage": enrollment.attendance_percentage,
    }