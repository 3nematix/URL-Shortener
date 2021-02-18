from .models import Link
from .forms import UrlForm
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from ratelimit.decorators import ratelimit
from .exceptions import KeyInvalid, LinkInActive, LinkExpired
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect


def urlParam(key='', keyUrlParam=''):
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


def validation(f):
    def wrapper(request, short_url, *args, **kwargs):
        try:
            link = Link.objects.get(short_url=short_url)

            if link.key is not None:
                key = request.GET.get('key', None)
                if not key == link.key:
                    raise KeyInvalid

            if link.is_active != True:
                raise InActiveLink

            if timezone.localtime(timezone.now()) > link.date_expires.astimezone(timezone.get_current_timezone()):
                raise LinkExpired

            return f(request, short_url, link, *args, **kwargs)

        except ObjectDoesNotExist:
            messages.error(request, 'This <b>url</b> is invalid.')
            return redirect('home')

        except KeyInvalid:
            messages.error(request, 'This <b>url key</b> is invalid.')
            return redirect('home')

        except LinkInActive:
            messages.error(request, 'This <b>url</b> is in-active.')
            return redirect('home')

        except LinkExpired:
            messages.error(request, 'This <b>url</b> is expired.')
            return redirect('home')

    return wrapper


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


@validation
def info_about_url(request, short_url, link):
    form = UrlForm()
    keyUrlParam = urlParam(link.key)

    context = {
        'form': form,
        'url': link,
        'short_url': request.build_absolute_uri('/') + link.short_url + keyUrlParam
    }

    return render(request, 'index.html', context)


@validation
def redirect_to_url(request, short_url, link):

    if visitor_ip_address(request) != link.ip_address:
        link.new_view()

    return redirect(link.full_url)
