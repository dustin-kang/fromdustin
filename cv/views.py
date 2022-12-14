from django.shortcuts import render

def landing(request):
    return render(
        request,
        'cv/landing.html'
    )

def cv(request):
    return render(
        request,
        'cv/cv.html'
    )
