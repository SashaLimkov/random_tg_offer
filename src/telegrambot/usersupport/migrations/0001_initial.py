# Generated by Django 4.0.4 on 2022-04-16 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.BigIntegerField(unique=True, verbose_name='UserID')),
                ('name', models.CharField(max_length=255, verbose_name='UserName')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='UserQuestion',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=4000, verbose_name='Вопрос')),
                ('history', models.CharField(max_length=10000, null=True, verbose_name='История вопроса')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersupport.telegramuser', verbose_name='Пользователь')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PinnedMessage',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('kurators_chat', models.BigIntegerField(verbose_name='id вопроса у кураторов')),
                ('mentors_chat', models.BigIntegerField(verbose_name='id вопроса у наставников')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='usersupport.userquestion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('telegramuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='usersupport.telegramuser')),
                ('user_role', models.CharField(max_length=255, verbose_name='Роль')),
                ('telegram_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='User', to='usersupport.telegramuser', verbose_name='Пользователь')),
            ],
            options={
                'abstract': False,
            },
            bases=('usersupport.telegramuser',),
        ),
    ]
