# Generated by Django 2.0.4 on 2018-04-29 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='ad_pic/bat.png', upload_to='ad_pic/')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('price', models.FloatField(default=0.0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='CounterOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer', models.FloatField(default=0.0)),
                ('comment', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=0)),
                ('ad_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Advertisement')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify_type', models.IntegerField(default=0)),
                ('read_status', models.BooleanField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ad_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.Advertisement')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('email', models.CharField(default='xyz@gmail.com', max_length=100)),
                ('image', models.ImageField(default='pic_folder/user.png', upload_to='pic_folder/')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_name', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='followed_tags',
            field=models.ManyToManyField(to='app.Tag'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='notification_buyer', to='app.Profile'),
        ),
        migrations.AddField(
            model_name='notification',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='notification_seller', to='app.Profile'),
        ),
        migrations.AddField(
            model_name='counteroffer',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='tags',
            field=models.ManyToManyField(to='app.Tag'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile'),
        ),
    ]
