from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Post, Subscriber
from django.template.loader import render_to_string
import datetime
from django.utils import timezone






@shared_task
def send_email_task(pk):
    instance = Post.objects.get(pk=pk)
    emails = User.objects.filter(subscriptions__category__in=instance.postCategory.all()).values_list('email', flat=True)

    subject = f'Новая публикация в категории {":".join(category.name for category in instance.postCategory.all())}'

    text_content = (
        f'Публикация: {instance.title}\n'
        f'Текст: {instance.preview()}\n\n'
        f'Ссылка на публикацию: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )

    html_content = (
        f'Заголовок: {instance.title}<br>'
        f'Текст: {instance.preview()}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Перейти</a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def send_news_last_week():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)

    categories = set(posts.values_list('postCategory__name', flat=True))

    subscribers = set(Subscriber.objects.filter(category__name__in=categories).values_list('user__email', flat=True))

    html_content = render_to_string('daily_post.html',
                                    {'link': settings.SITE_URL,
                                     'posts': posts})

    msg = EmailMultiAlternatives(
        subject="Публикации за  последнюю неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers)

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
