from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property
from .utils import get_all_properties

def property_list(request):
    properties = get_all_properties()
    return JsonResponse({"data": properties})
