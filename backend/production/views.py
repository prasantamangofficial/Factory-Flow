from django.shortcuts import render


def production(request):
    return render(request, "production.html")