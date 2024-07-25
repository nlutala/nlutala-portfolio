from django.shortcuts import render
from django.http import FileResponse
from django.views.decorators.csrf import csrf_protect
from .models import HangmanGames, HangmanGuesses, TTTMoves
from .projects.pdf_merger import PDFMerger
from .projects.password_generator import PasswordGenerator
from .projects.hangman import Hangman
from .projects.random_letter import RandomLetter
from .projects.random_hangman_word import RandomHangmanWord
from .projects.gamestate_ttt import GameState
from .projects.ml_cpu_ttt import MLCPU
import os, time

# Create your views here.


def index(request):
    """
    Returns the homepage of the website.
    """
    return render(request, "website/index.html")


def projects(request):
    """
    Returns a page with a list of projects to try out.
    """
    return render(request, "website/projects.html")


@csrf_protect
def pdf_merger(request):
    """
    Returns a page with a demo of the PDF Merger project to try out.
    """
    merger = PDFMerger()
    BASE_DIR = merger.get_base_dir()

    if request.method == "POST":
        pdfs = [file.name for file in request.FILES.getlist("formFileMultiple")]

        for file in request.FILES.getlist("formFileMultiple"):
            file_path = os.path.join(BASE_DIR, file.name)
            with open(file_path, "wb+") as new_file:
                for chunk in file.chunks():
                    new_file.write(chunk)

        try:
            merger.add_pdf_files(pdfs)
            filename = merger.merge_pdfs(request.POST.get("mergedFileName"))
        except ValueError as error_message:
            for file in os.listdir(BASE_DIR):
                if file.endswith(".pdf"):
                    os.remove(os.path.join(BASE_DIR, file))
            return render(
                request, "website/pdf_merger.html", {"error_message": error_message}
            )

        if filename.endswith(".pdf"):
            pdf = open(filename, "rb")
        else:
            pdf = open(f"{filename}.pdf", "rb")

        response = FileResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{filename}"'
        return response
    else:
        for file in os.listdir(BASE_DIR):
            if file.endswith(".pdf"):
                os.remove(os.path.join(BASE_DIR, file))

    return render(request, "website/pdf_merger.html")


@csrf_protect
def password_generator(request):
    """
    Returns a page with a demo of the password generator to try out.
    """
    pg = PasswordGenerator(8)
    warning_text = ""

    if request.method == "POST":
        length = int(request.POST.get("passwordLength"))
        num_numbers = int(request.POST.get("numNumbers"))
        num_symbols = int(request.POST.get("numSymbols"))
        num_uppercase = int(request.POST.get("numUppercase"))

        try:
            passwords = pg.generate_password(
                length=length,
                num_numbers=num_numbers,
                num_symbols=num_symbols,
                num_uppercase=num_uppercase,
            )
        except ValueError as text:
            warning_text = text
            passwords = pg.generate_password(
                num_numbers=2, num_symbols=2, num_uppercase=2
            )
    else:
        passwords = pg.generate_password(num_numbers=2, num_symbols=2, num_uppercase=2)

    return render(
        request,
        "website/password_generator.html",
        {"passwords": passwords, "warning_text": warning_text},
    )


@csrf_protect
def hangman_template(request):
    """
    Returns a page with instructions and allows the user to
    select a level to play the hangman game.
    """
    # Initialise the level
    level = ""

    # Initialise the hangman guesser
    hangman = Hangman()

    # Initialise hidden word
    words = HangmanGames.objects.values_list("word", flat=True)

    # Take the most recent word added to the database/model for the user to guess
    if len(words) != 0:
        hangman_word = words[len(words) - 1]
        hidden_word = "_ " * len(hangman_word)
        hidden_word = hidden_word[: len(hidden_word) - 1]

    # Initialise previous guesses
    previous_guesses = hangman.getIncorrectGuesses()

    # alert user won or lost
    alert_message = ""

    if request.method == "POST":
        level = request.POST.get("level")

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

            HangmanGames.objects.all().delete()

            hangman_db = HangmanGames.objects.create(
                level=level.upper(),
                word=hangman_word,
                guesses_allowed=number_of_guesses,
                guesses_taken=0,
            )
            hangman_db.save()

            return render(
                request,
                "website/hangman_game.html",
                {
                    "level": level,
                    "hidden_word": hidden_word,
                    "number_of_guesses": number_of_guesses,
                    "previous_guesses": previous_guesses,
                },
            )
        else:
            level = HangmanGames.objects.get(word=hangman_word).level.capitalize()
            user_guess = request.POST.get("letterWordGuess")

            HangmanGuesses.objects.create(
                foreign_key=HangmanGames.objects.get(word=hangman_word).id,
                guess=user_guess,
            )

            foreign_key = HangmanGames.objects.get(word=hangman_word).id
            guesses = HangmanGuesses.objects.filter(
                foreign_key=foreign_key
            ).values_list("guess", flat=True)

            for guess in guesses:
                hidden_word = hangman.revealCorrectLetters(hangman_word, guess)

            previous_guesses = hangman.getIncorrectGuesses()

            guesses_taken = (
                HangmanGames.objects.get(word=hangman_word).guesses_taken + 1
            )

            HangmanGames.objects.filter(word=hangman_word, id=foreign_key).update(
                guesses_taken=guesses_taken
            )

            guesses_allowed = HangmanGames.objects.get(
                word=hangman_word
            ).guesses_allowed
            number_of_guesses_remaining = guesses_allowed - guesses_taken

            if hidden_word == hangman_word:
                alert_message = f"""
                Congratulations!
                You have guessed the word in {guesses_taken} guess(es)!
                """
            elif guesses_taken == guesses_allowed:
                alert_message = f"""
                    Unlucky!
                    The word was: {hangman_word}
                    """

            return render(
                request,
                "website/hangman_game.html",
                {
                    "level": level,
                    "hidden_word": " ".join(list(hidden_word)),
                    "number_of_guesses": number_of_guesses_remaining,
                    "previous_guesses": previous_guesses,
                    "alert_message": alert_message,
                },
            )

    return render(request, "website/hangman.html")


def tic_tac_toe_helper(gs: GameState) -> str:
    """
    Takes a GameState as a parameter and returns a message
    if the tic-tac-toe game has ended.
    """
    # Check whether the game is done... again
    if gs.is_done():
        if gs.outcome == "W":
            return "Unlucky! The CPU won this time."
        elif gs.outcome == "L":
            return "Great job! You won!"
        else:
            return "It is a draw this time. Why not play again?"
    else:
        return ""


@csrf_protect
def tic_tac_toe(request):
    """
    Returns a page with a demo of the toc-tac-toe game to try out.
    """
    cpu = MLCPU()
    gs = GameState()

    info_grid = []

    for i in range(len(gs.get_game_state())):
        if gs.get_game_state()[i] == "_":
            info_grid.append(i)

    info_grid_rows = []

    game_over_message = tic_tac_toe_helper(gs)

    if request.method == "POST":
        user_position = int(request.POST.get("position"))
        game_state = TTTMoves.objects.values_list("game_state", flat=True)
        state = game_state[len(game_state) - 1]
        game_state_id = TTTMoves.objects.get(game_state=state).id

        for i in range(len(list(state))):
            if list(state)[i] != "_":
                gs.set_game_state(i, list(state)[i])

        gs.set_game_state(user_position, "O")

        # Check whether the game is done
        game_over_message = tic_tac_toe_helper(gs)

        if game_over_message == "":
            # Just to make the effect that the CPU is "thinking" before making a move
            time.sleep(1)
            cpu_position = cpu.make_move(
                list(gs.get_game_state()), gs.get_available_positions()
            )
            gs.set_game_state(cpu_position, cpu.get_symbol())

            # Check whether the game is done... again
            game_over_message = tic_tac_toe_helper(gs)

        TTTMoves.objects.filter(id=game_state_id).update(
            game_state="".join(gs.get_game_state())
        )
    else:
        TTTMoves.objects.all().delete()
        # Create new entry in TTTMoves
        ttt_db = TTTMoves.objects.create(
            game_state="".join(gs.get_game_state()), outcome=""
        )
        ttt_db.save()

    grid = gs.get_game_state()
    grid_rows = []

    for i in range(0, len(grid), 3):
        grid_rows.append(grid[i : i + 3])
        info_grid_rows.append(info_grid[i : i + 3])

    available_spaces = gs.get_available_positions()

    return render(
        request,
        "website/tic_tac_toe.html",
        {
            "grid_rows": grid_rows,
            "info_grid": info_grid,
            "info_grid_rows": info_grid_rows,
            "game_over_message": game_over_message,
            "available_spaces": available_spaces,
        },
    )
