from django.shortcuts import render
from django.http import FileResponse
from .projects.pdf_merger import PDFMerger
from .projects.password_generator import PasswordGenerator
from .projects.hangman import Hangman
from .projects.random_letter import RandomLetter
from .projects.random_hangman_word import RandomHangmanWord
import os

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
    Returns a page with a demo of the PDF Merger project to try out.
    '''
    merger = PDFMerger()
    BASE_DIR = merger.get_base_dir()
    
    if request.method == "POST":
        pdfs = [file.name for file in request.FILES.getlist('formFileMultiple')]
        
        if len(pdfs) < 2:
            return render(request, "website/pdf_merger.html")
        
        for file in request.FILES.getlist('formFileMultiple'):
            file_path = os.path.join(BASE_DIR, file.name)
            with open(file_path, 'wb+') as new_file:
                for chunk in file.chunks():
                    new_file.write(chunk)
        
        merger.add_pdf_files(pdfs)
        filename = merger.merge_pdfs(request.POST.get('mergedFileName'))
        
        if filename.endswith(".pdf"):
            pdf = open(filename, 'rb')
        else:
            pdf = open(f'{filename}.pdf', 'rb')
            
        response = FileResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
    else:
        for file in os.listdir(BASE_DIR):
            if file.endswith(".pdf"):
                os.remove(os.path.join(BASE_DIR, file))
        
    return render(request, "website/pdf_merger.html")

def password_generator(request):
    '''
    Returns a page with a demo of the password generator to try out.
    '''
    pg = PasswordGenerator(8)
    display_warning = False
    warning_text = ""

    if request.method == "POST":
        length = int(request.POST.get('passwordLength'))
        num_numbers = int(request.POST.get('numNumbers'))
        num_symbols = int(request.POST.get('numSymbols'))
        num_uppercase = int(request.POST.get('numUppercase'))

        try:
            passwords = pg.generate_password(
                length=length, num_numbers=num_numbers, 
                num_symbols=num_symbols, num_uppercase=num_uppercase
                )
        except ValueError as text:
            display_warning = True
            warning_text = text
            passwords = []
    else:
        passwords = pg.generate_password(
            num_numbers=2, num_symbols=2, num_uppercase=2
            )

    if display_warning == True:
        return render(request, "website/password_generator.html", {
            "passwords": passwords, 
            "display_warning": display_warning, 
            "warning_text": warning_text
            })

    return render(request, "website/password_generator.html", {
        "passwords": passwords, 
        "display_warning": display_warning, 
        "warning_text": warning_text
        })

def hangman_template(request):
    '''
    Returns a page with instructions and allows the user to
    select a level to play the hangman game.
    '''
    if request.method == "POST":
        level = request.POST.get('level')
        return render(request, "website/hangman_game.html", {"level": level})

    return render(request, "website/hangman.html")

def hangman_game(request):
    # TODO: Finish implementation
    '''
    Returns a page with a demo of the hangman game.
    '''
    if level == None:
        render(request, "website/hangman.html")

    if request.method == "POST":
        level = request.POST.get('level').upper()
        render(request, "website/hangman_game.html")

def contact(request):
    '''
    Returns a page with where to contact/follow me (Github & LinkedIn).
    '''
    return render(request, "website/contact.html")
