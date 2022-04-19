# Generated by Django 4.0.4 on 2022-04-16 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersupport', '0002_rename_question_id_pinnedmessage_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquestion',
            name='feedback',
            field=models.CharField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='userquestion',
            name='helper_id',
            field=models.BigIntegerField(default=0, verbose_name='ID Отвечающего'),
        ),
        migrations.AddField(
            model_name='userquestion',
            name='rate',
            field=models.CharField(max_length=1, null=True, verbose_name='Оценка'),
        ),
        migrations.AddField(
            model_name='userquestion',
            name='state',
            field=models.CharField(default='Открытый вопрос', max_length=100, verbose_name='Состояние'),
        ),
        migrations.AlterField(
            model_name='userquestion',
            name='question',
            field=models.CharField(max_length=5000, verbose_name='Вопрос'),
        ),
    ]
