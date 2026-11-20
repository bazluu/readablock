from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_usermeta_daily_word_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermeta',
            name='free_access',
            field=models.BooleanField(default=False, help_text='Grants full app access without a subscription.'),
        ),
    ]
