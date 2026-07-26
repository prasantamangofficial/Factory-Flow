from django.shortcuts import render


def raw_materials(request):
    return render(request, "raw_materials.html")