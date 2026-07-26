from django.shortcuts import render


def expenses(request):
    return render(request, "expenses.html")