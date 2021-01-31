from .models import Link
from .forms import UrlForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
def index(request):
    form = UrlForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            key = request.POST.get('key')
            full_url = request.POST.get('url')

            link = form.save()
            link.save()

            messages.success(
                request, f"Your <b>URL</b> was successfully created!")
            context['url'] = request.build_absolute_uri() + link.short_url
        else:
            messages.error(request, 'An error occured 😔')

    return render(request, 'index.html', context)


def info_about_url(request, short_url):
    try:
        form = UrlForm()
        link = Link.objects.get(short_url=short_url)
        context = {
            'form': form,
            'url': link,
            'short_url': request.build_absolute_uri('/') + link.short_url
        }
    except ObjectDoesNotExist:
        messages.error(request, 'This <b>URL</b> was not found!')

    return render(request, 'index.html', context)


def redirect_to_url(request, short_url):
    key = request.GET.get('key', None)
    link = get_object_or_404(Link, short_url=short_url)

    if link.key is not None:
        if not key == link.key:
            messages.add_message(
                request,
                messages.ERROR,
                'This url requires a key...'
            )
            return render(request, 'index.html')

    link.new_view()
    return redirect(link.full_url)
