import requests
from django.http import HttpResponse
from django.shortcuts import render
from .models import Therapist


def index(request):
    therapist = Therapist.objects.all()
    for t in therapist:
        slug = t.pk
        print(slug)
    return render(request, 'index.html', {'names': therapist})


def therapist_page(request, therapist_id):
    therapist = Therapist.objects.get(id=therapist_id)
    name = therapist.name
    photo = therapist.photo_link
    methods = therapist.methods[1:-1].split(',')
    return render(request, 'therapist_page.html', {'name': name, 'methods': methods, 'photo': photo})
