from django.shortcuts import render
import markdown2 
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, page):
    return render(request, "encyclopedia/pages.html", {
        "page" : markdown2.markdown(util.get_entry(page)),
        "name" : page
    })
