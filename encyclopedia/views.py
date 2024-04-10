from django.shortcuts import render
import markdown as md
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

from . import util, forms


def index(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    filtered_entries = [
        entry for entry in entries if query.lower() in entry.lower()]

    if len(filtered_entries) == 1 and query.lower() == filtered_entries[0].lower():
        return HttpResponseRedirect(
            reverse("encyclopedia:wiki", kwargs={"TITLE": query})
        )

    return render(request, "encyclopedia/index.html", {
        "entries": filtered_entries
    })


def wiki(request, TITLE):
    entry = util.get_entry(TITLE)
    if not entry:
        # return render(request, "encyclopedia/404.html", {"title": TITLE})
        msg = f"Requested page {TITLE} doesnt exist"
        return render(request, "encyclopedia/error.html", {
            "code": 404,
            "message": msg
        })

    content = md.markdown(entry)
    return render(request, "encyclopedia/wiki.html", {
        "title": TITLE,
        "content": content
    })


def add(request):
    if request.method == "POST":
        newform = forms.NewArticleForm(request.POST)

        if newform.is_valid():
            title = newform.cleaned_data["title"]
            content = newform.cleaned_data["content"]

            if util.get_entry(title):
                msg = "Requested page already exists"
                return render(request, "encyclopedia/error.html", {
                    "code": 409,
                    "message": msg
                })

            util.save_entry(title, content)

            return HttpResponseRedirect(
                reverse("encyclopedia:wiki", kwargs={"TITLE": title})
            )
        else:
            return render(request, "encyclopedia/add.html", {
                "form": newform
            })

    return render(request, "encyclopedia/add.html", {
        "form": forms.NewArticleForm()
    })


def edit(request, TITLE):
    if request.method == "POST":
        editform = forms.EditArticleForm(request.POST)
        if editform.is_valid():
            content = editform.cleaned_data['content']

            if not util.get_entry(TITLE):
                msg = "Bad request"
                return render(request, "encyclopedia/error.html", {
                    "code": 400,
                    "message": msg
                })

            util.save_entry(TITLE, content)
            return HttpResponseRedirect(
                reverse("encyclopedia:wiki", kwargs={"TITLE": TITLE})
            )
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": TITLE,
                "form": editform
            })

    content = util.get_entry(TITLE)
    form = forms.EditArticleForm({"content": content})
    return render(request, "encyclopedia/edit.html", {
        "title": TITLE,
        "form": form
    })


def random_page(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(
        reverse("encyclopedia:wiki", kwargs={"TITLE": title})
    )
