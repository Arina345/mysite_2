from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return HttpResponse(
        """<html><title> Сайт Арины Крикуновой </title><h1> Арина Крикунова </h1</html>"""
    )
