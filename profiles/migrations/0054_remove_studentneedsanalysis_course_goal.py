from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0053_remove_studentneedsanalysis_self_study_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studentneedsanalysis",
            name="course_goal",
        ),
    ]