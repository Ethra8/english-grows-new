from django.db import migrations, models
import django.db.models.deletion


def verify_empty_snapshots(apps, schema_editor):
    Snapshot = apps.get_model("profiles", "StudentSkillTermSnapshot")

    if Snapshot.objects.using(schema_editor.connection.alias).exists():
        raise RuntimeError(
            "Cannot make term snapshot fields required: existing records "
            "must be reviewed before applying this migration."
        )


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0059_studenttermsubskillassessment_and_more"),
    ]

    operations = [
        migrations.RunPython(
            verify_empty_snapshots,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="studentskilltermsnapshot",
            name="term_assessment",
            field=models.ForeignKey(
                default=None,
                to="profiles.studenttermassessment",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="skill_snapshots",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="studentskilltermsnapshot",
            name="skill",
            field=models.CharField(
                default=None,
                max_length=20,
                choices=[
                    ("speaking", "Speaking"),
                    ("reading", "Reading"),
                    ("writing", "Writing"),
                    ("listening", "Listening"),
                ],
            ),
            preserve_default=False,
        ),
    ]