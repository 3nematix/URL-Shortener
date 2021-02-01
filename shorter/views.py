from .models import Link
from .forms import UrlForm
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from ratelimit.decorators import ratelimit
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect


def urlParam(key=''):
    keyUrlParam = ''
    if key and len(key) > 1:
        keyUrlParam = f'/?key={key}'

    return keyUrlParam


def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@ratelimit(key='ip', rate='2/m', method='POST')
def index(request):
    was_limited = getattr(request, 'limited', False)
    form = UrlForm()
    context = {
        'form': form
    }

    if was_limited:
        messages.error(
            request, ' You can generate 2 links in one minute, please wait.')
        return render(request, 'index.html', context)

    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            key = request.POST.get('key')
            keyUrlParam = urlParam(key)

            link = form.save(commit=False)
            link.ip_address = visitor_ip_address(request)
            link.save()

            full_url = request.build_absolute_uri(
            ) + link.short_url + keyUrlParam
            context['url'] = full_url

            messages.success(
                request, f"Your <b>URL</b> was successfully created! <a class='text-success font-weight-bold' href='{full_url}'>{full_url}</a>")

        else:
            messages.error(request, 'An error has occured...')

    return render(request, 'index.html', context)


def info_about_url(request, short_url):
    try:
        form = UrlForm()
        key = request.GET.get('key', None)
        link = Link.objects.get(short_url=short_url)
        keyUrlParam = urlParam(link.key)

        context = {
            'form': form,
            'url': link,
            'short_url': request.build_absolute_uri('/') + link.short_url + keyUrlParam
        }

        if timezone.localtime(timezone.now()) > link.date_expires.astimezone(timezone.get_current_timezone()):
            messages.error(request, 'This link is expired.')
            return render(request, 'index.html')

        if link.is_active != True:
            messages.error(request, 'This link is invalid.')
            return render(request, 'index.html')

        if link.key is not None:
            if not key == link.key:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'This <b>URL</b> requires a key!'
                )
                return render(request, 'index.html')

    except ObjectDoesNotExist:
        messages.error(request, 'This <b>URL</b> was not found!')

    return render(request, 'index.html', context)


def redirect_to_url(request, short_url):
    key = request.GET.get('key', None)
    link = get_object_or_404(Link, short_url=short_url)

    if timezone.localtime(timezone.now()) > link.date_expires.astimezone(timezone.get_current_timezone()):
        messages.error(request, 'This link is expired.')
        return render(request, 'index.html')

    if link.is_active != True:
        messages.error(request, 'This link is invalid.')
        return render(request, 'index.html')

    if link.key is not None:
        if not key == link.key:
            messages.add_message(
                request,
                messages.ERROR,
                'This <b>URL</b> requires a valid key!'
            )
            return render(request, 'index.html')

    if visitor_ip_address(request) != link.ip_address:
        link.new_view()

    return redirect(link.full_url)
