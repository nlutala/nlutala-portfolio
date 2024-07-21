from django.shortcuts import render
from django.http import FileResponse
from .projects.pdf_merger import PDFMerger
import os

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


def pdf_merger(request):
    """
    Returns a page with a the PDF Merger project to try out.
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


def contact(request):
    """
    Returns a page with where to contact/follow me (Github & LinkedIn).
    """
    return render(request, "website/contact.html")
