from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

"""connecto airtable database"""
AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
             'Movies',
             api_key=os.environ.get('AIRTABLE_API_KEY'))
# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" +
                               user_query.lower() + "', LOWER({Name}))")

    context = {"search_result": search_result}
    return render(request, 'movies/movies_stuff.html',
                 context)

def about(request):
    return render(request,'movies/about.html')

def create(request):
    if request.method == 'POST':
        data = {
            'Name' : request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url')}],
            'Rating': int(request.POST.get('rating')),
            'Notes':request.POST.get('notes')
        }

        AT.insert(data)
    return redirect('/')

"""edit movie function"""
def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url')}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        AT.update(movie_id, data)
    return redirect('/')
