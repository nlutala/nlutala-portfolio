from django.shortcuts import render
from .forms import PDFMergerForm

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
    if request.method == "POST":
        form = PDFMergerForm(request.POST)
        if form.is_valid():
            return render(request, "website/pdf_merger_1.html")
    else:
        form = PDFMergerForm()
        
    return render(request, "website/pdf_merger.html", {"form" : form})

def contact(request):
    '''
    Returns a page with where to contact/follow me (Github & LinkedIn).
    '''
    return render(request, "website/contact.html")
