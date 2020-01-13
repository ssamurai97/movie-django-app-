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
        try:

            response = AT.insert(data)
            messages.success(request,"New movie has been Added: {}".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request,"Got an error when try to create a movie: {}".format(e))
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

        try:

            response = AT.update(movie_id, data)
            messages.success(request, 'Updated movie: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, "Error while updating {}".format(e))
    return redirect('/')

def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        cresponse = AT.delete(movie_id)
        messages.warning(request,"Deleted movie: {}".format(movie_name))
    except Exception as e:
        messages.warning(request, 'Error while deleting the a movie: {}'.format(e))

    return redirect('/')
