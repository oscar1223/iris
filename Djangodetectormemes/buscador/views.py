import json
import zlib

import requests

from buscador.forms import searchDataForm
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import generic
from modules.mongo import find_words


def index(request):
    #return render(request, 'buscador/detail.html')
    result = find_words("ANTONIO")
    result[0].pop('_id')
    print(result)
    return JsonResponse({"response": result})



def retrieve_image(word,source):
    r = requests.get(f'http://127.0.0.1:5000/images?word={word}&source={source}')
    print(r)
    data = r.json()
    img_tag = ''
    memes = []
    for img in data:
        img_tag = img_tag+'<img id="foto" alt="sample" src="data:image/png;base64,{0}">'.format(data[img])
        memes.append(data[img])

    return memes
    #return HttpResponse(img_tag)


def send_query_db(request, word):
    memes = retrieve_image(word)

    return render(request, 'buscador/index.html', {'memes' : memes})



class MainView(generic.FormView):
    template_name = 'buscador/index.html'
    form_class = searchDataForm

    def get(self, request, *args, **kwargs):

        form = searchDataForm
        return render(request, 'buscador/index.html', {'form': form})

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':

            form = self.form_class(request.POST)

            if form.is_valid():
                print("valid")
                keyword = form.cleaned_data['keyword']
                source = form.cleaned_data['source']
                context = {
                    'form': form,
                    'word': retrieve_image(keyword,source),
                }
                return render(request, 'buscador/index.html', context)

            else:
                form = searchDataForm()
            context = {
                'form': form,
            }
            return render(request, 'buscador/index.html', context)









































