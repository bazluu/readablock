from django.db import migrations

PLANS = [
    {
        "name": "Basic - Annually",
        "code": "PLN_uuowdtv63zpwzvw",
        "amount": 120000,  # ZAR 1,200.00
        "currency": "ZAR",
        "interval": "annually",
    },
    {
        "name": "Basic - Monthly",
        "code": "PLN_2z6q5a6h3x567wk",
        "amount": 12000,  # ZAR 120.00
        "currency": "ZAR",
        "interval": "monthly",
    },
]


def seed_plans(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")

    for plan in PLANS:
        Plan.objects.update_or_create(code=plan["code"], defaults=plan)


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_plans, migrations.RunPython.noop),
    ]
