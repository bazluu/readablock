from django.db import migrations, models


def backfill_furthest_read(apps, schema_editor):
    """Set each existing reader's furthest position to their current position.

    Without this, readers who have already progressed through a book would see
    sentences 0..sentence_last_read counted as "new" on their next forward turn,
    re-inflating the daily reading log retroactively.
    """
    BookProgress = apps.get_model("app", "BookProgress")
    BookProgress.objects.update(sentence_furthest_read=models.F("sentence_last_read"))


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0018_alter_readinglog_word_count_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookprogress",
            name="sentence_furthest_read",
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(backfill_furthest_read, migrations.RunPython.noop),
    ]