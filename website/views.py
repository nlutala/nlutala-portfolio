from django.shortcuts import render
from django.http import FileResponse
from .models import HangmanGames, HangmanGuesses
from .projects.pdf_merger import PDFMerger
from .projects.password_generator import PasswordGenerator
from .projects.hangman import Hangman
from .projects.random_letter import RandomLetter
from .projects.random_hangman_word import RandomHangmanWord
import os, datetime

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
    # Initialise the level
    level = ""
    # Initialise the hangman guesser
    hangman = Hangman()
    # Initialise hidden word
    words = HangmanGames.objects.values_list("word", flat=True)

    if len(words) != 0:
        hangman_word = words[len(words)-1]
        hidden_word = "_ " * len(hangman_word)
        hidden_word = hidden_word[:len(hidden_word)-1]

    # Initialise number of guesses
    number_of_guesses = 0
    # Initialise previous guesses
    previous_guesses = hangman.getIncorrectGuesses()

    # alert user won or lost
    alert_message = ""

    if request.method == "POST":
        level = request.POST.get('level')

        if level != None:
            letter = RandomLetter().generateRandomLetter()
            hangman_word = RandomHangmanWord(level.upper()).generateRandomWord(letter)

            if level == "Easy":
                number_of_guesses = len(hangman_word) + 7
            elif level == "Medium":
                number_of_guesses = len(hangman_word) + 5
            else:
                number_of_guesses = len(hangman_word) + 3

            hidden_word = "_ " * len(hangman_word)

            # print(HangmanGames.objects.values_list("word", flat=True))
            # Below deletes everything from the table
            HangmanGames.objects.all().delete()
            hangman_db = HangmanGames.objects.create(
                level=level.upper(),
                word=hangman_word,
                guesses_allowed=number_of_guesses,
                guesses_taken=0
            )
            hangman_db.save()

            return render(request, "website/hangman_game.html", {
                "level": level, "hidden_word": hidden_word,
                "number_of_guesses": number_of_guesses, 
                "previous_guesses": previous_guesses
            })
        else:
            level = HangmanGames.objects.get(word=hangman_word).level.capitalize()
            user_guess = request.POST.get('letterWordGuess')
            HangmanGuesses.objects.create(
                foreign_key=HangmanGames.objects.get(word=hangman_word).id,
                guess=user_guess
            )
            foreign_key = HangmanGames.objects.get(word=hangman_word).id
            guesses = HangmanGuesses.objects.filter(
                foreign_key=foreign_key
                ).values_list(
                    "guess", flat=True
                )

            for guess in guesses:
                hidden_word = hangman.revealCorrectLetters(hangman_word, guess)
            
            previous_guesses = hangman.getIncorrectGuesses()

            guesses_taken = HangmanGames.objects.get(word=hangman_word).guesses_taken + 1
            HangmanGames.objects.filter(
                word=hangman_word, id=foreign_key
                ).update(
                    guesses_taken=guesses_taken
                )
            guesses_allowed = HangmanGames.objects.get(word=hangman_word).guesses_allowed

            print("Guesses taken:", guesses_taken, "\nGuesses allowed:", guesses_allowed)

            if hidden_word == hangman_word:
                alert_message = f'''
                Congratulations!
                You have guessed the word in {guesses_taken} guess(es)!
                '''
            elif guesses_taken == guesses_allowed:
                alert_message = f'''
                    Unlucky!
                    The word was: {hangman_word}
                    '''

            return render(request, "website/hangman_game.html", {
                "level": level, "hidden_word": " ".join(list(hidden_word)),
                "number_of_guesses": number_of_guesses, 
                "previous_guesses": previous_guesses,
                "alert_message": alert_message
            })

    return render(request, "website/hangman.html")

def contact(request):
    '''
    Returns a page with where to contact/follow me (Github & LinkedIn).
    '''
    return render(request, "website/contact.html")
