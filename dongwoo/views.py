from django.shortcuts import render

def landing(request):
    return render(
        request,
        'dongwoo/landing.html'
    )

def page_not_found(request, exception):
    return render(request, 'dongwoo/404.html', {})

def server_error(request, exception):
    return render(request, 'dongwoo/500.html', {})