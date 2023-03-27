from django.shortcuts import render
from django import forms
import random
import markdown
import re

from . import util

class AddPage(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'name':'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'name':'content','rows':3,'cols':8}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def newpage(request):
    exist = util.list_entries()
    if request.method == 'POST':
        form = AddPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']    
            if title not in exist:          
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html",{
                    "page": util.get_entry(title),
                    "entry": title
                })          
            else:
                message = f"Error: {title} already exists"
                return render(request, "encyclopedia/newpage.html",{
                "form": message
                })
    return render(request, "encyclopedia/newpage.html",{
        "form": AddPage()
    })

def randompage(request):
    entry = util.list_entries()
    page = random.choice(entry)

    return render(request, "encyclopedia/entry.html",{
        "page": util.get_entry(page),
        'entry': page
    })

def entry(request, page):
    if request.method == "GET":
        requested = util.list_entries()
        if page in requested:
            return render(request, "encyclopedia/entry.html",{
                "page": util.get_entry(page),
                'entry': page
            })
        else:
            nopage = f"No page called {page} available"
            return render(request, "encyclopedia/entry.html",{
                "page": nopage
            })
    else:
        form = AddPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html",{
                "page": util.get_entry(title),
                'entry': title
            })
    return render (request, "encyclopedia/newpage.html")

def editpage(request, page):
    if request.method == 'POST':
            form = AddPage(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                return render(request, "encyclopedia/entry.html",{
                    "page": util.get_entry(title),
                    "entry": title
                })      
    pageedit = util.get_entry(page)
    return render(request, "encyclopedia/editpage.html",  {
        "form": AddPage(initial={'title':page,'content':pageedit})
    })

def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    message = f"{query} not in wiki!"
    #if request.method == 'get':
    if query in entries:
        return render(request, "encyclopedia/entry.html", {
            "page": util.get_entry(query),
            "entry": query
        })
    else :#query not in entries:
        pattern = re.compile(f".*{query}")
        text = util.list_entries()
        results = list(filter(pattern.match, text))
        return render(request, "encyclopedia/search.html",{
            "results": results,
            "message": message
    })
    # else:
    #     message = f"{query} not in wiki!"
    #     return render(request, "encyclopedia/search.html",{
    #         "message": message
    # })
