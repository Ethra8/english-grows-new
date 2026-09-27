from django.db import migrations, models
import django.db.models.deletion


def remove_legacy_snapshots(apps, schema_editor):
    """
    Remove obsolete test snapshots from the previous assessment
    structure before requiring the new Formal Term Assessment fields.

    Preserve snapshots already associated with a Formal Term Assessment.
    """
    Snapshot = apps.get_model("profiles", "StudentSkillTermSnapshot")
    db = schema_editor.connection.alias

    # Legacy snapshots have no Formal Term Assessment relationship.
    Snapshot.objects.using(db).filter(
        term_assessment__isnull=True
    ).delete()

    # Remaining snapshots must have a valid skill.
    if Snapshot.objects.using(db).filter(
        skill__isnull=True
    ).exists():
        raise RuntimeError(
            "Cannot make term snapshot fields required: "
            "some Formal Term Assessment snapshots have no skill."
        )


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ("profiles", "0059_studenttermsubskillassessment_and_more"),
    ]

    operations = [
        migrations.RunPython(
            remove_legacy_snapshots,
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