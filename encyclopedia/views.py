from django.shortcuts import render

from . import util
import markdown2
import entries
from random import choice

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def md_to_html(title):
    page = util.get_entry(title)
    if page == None:
        return None
    else:
        return markdown2.markdown(page)
    
def page(request, title):
    title2 = md_to_html(title)
    if title2 == None:
        return render(request,"encyclopedia/error.html" )
    else:
        return render(request, "encyclopedia/page.html", {
            "name": title2,
            "tit" : title.capitalize()
        } )
        
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        item = md_to_html(entry_search)
        if item != None:
            return render(request, "encyclopedia/page.html", {
                "tit" : entry_search,
                "name" : item
            })
        else:
            pages_filt = []
            entries2 = util.list_entries()
            entry_search2 = entry_search.upper()
            for i in entries2:
                kefalaia = i.upper()
                if entry_search2 in kefalaia:
                    pages_filt.append(i)
                if len(pages_filt) == 0 :
                    return render(request, "encyclopedia/errorexist.html",{
                        "error_message" : "Your requested page was not found."
                    } )
                    
            return render(request, "encyclopedia/filtpages.html", {
                "filtered_pages" : pages_filt, 
                "filter_phrase" : entry_search
            })
                    
                
def random(request):
    entries_stored = util.list_entries()
    rand_page = choice(entries_stored)
    
    return render(request, "encyclopedia/page.html", {
        "tit" :  rand_page ,
        "name" : md_to_html(rand_page)
    })


def newpage(request):
    if request.method == "GET":
        return render (request, "encyclopedia/newpage.html"
        )
    elif request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        listings = util.list_entries()
        for listing in listings:
            listing = listing.upper()
        titleup = title.upper()
        if titleup not in listings:
            util.save_entry(title, content)
            return render (request, "encyclopedia/page.html", {
                "tit" : title,
                "name" :markdown2.markdown(content)
            })
        else:
            return render (request, "encyclopedia/errorexist.html", {
                "error_message" : "Your requested page allready exists."
            })


def editpage(request):
    if request.method == "POST":
        title  = request.POST['title']
        content = request.POST['content']
        
        return render(request, "encyclopedia/edit.html", {
            "title" : title,
            "content" : util.get_entry(title)
        })
    


def savepage(request):
    
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return render (request, "encyclopedia/page.html", {
            "tit" : title,
            "name" : markdown2.markdown(content)
        })
