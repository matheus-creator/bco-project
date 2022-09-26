from django.http import JsonResponse

import json
import sys
sys.path.append('C:/Users/nedd8/Documents/Projetos de programação/interview-project/occupations/occupations/api')
from find_occupation import find_occupation

def index(request):
    occupation_response = process_data(request)
    return JsonResponse(occupation_response)

def process_data(request):
    jsonResponse = json.loads(request.body.decode('utf-8'))
    return find_occupation(jsonResponse)