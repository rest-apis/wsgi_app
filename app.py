#encoding=utf-8

from wsgi_layer import Application
import os

def echo(request):
    return request.GET['with'][0] + '\n'

def words(request, prefix):
    limit = request.GET['limit'] if 'limit' in request.GET else 10
    raw_results = os.popen("look %s"%prefix).readlines()[:limit]
    return ",\n".join([word.replace('\n','') for word in raw_results])

        
app = Application({
    '/echo': echo,
    '/words/with/(?P<prefix>\w+)': words
})

app.serve()
