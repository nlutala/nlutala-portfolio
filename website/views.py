from django.shortcuts import render

# Create your views here.

def index(request):
    '''
    Returns the homepage of the website.
    '''
    return render(request, "website/index.html")

def projects(request):
    '''
    Returns a page with a list of projects to try out.
    '''
    return render(request, "website/projects.html")

def pdf_merger(request):
    '''
    Returns a page with a the PDF Merger project to try out.
    '''
    return render(request, "website/pdf_merger.html")

def contact(request):
    '''
    Returns a page with where to contact/follow me (Github & LinkedIn).
    '''
    return render(request, "website/contact.html")
