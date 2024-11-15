from django.http import HttpResponse
from django.shortcuts import render

def streamlit_page(request):
    return render(request, 'caremi/home.html')