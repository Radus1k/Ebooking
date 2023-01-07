from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {"t": "This is a junk of random text"}
    return render(request, "base.html", context=context)
