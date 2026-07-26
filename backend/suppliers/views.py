from django.shortcuts import render


def suppliers(request):
    return render(request, "suppliers.html")