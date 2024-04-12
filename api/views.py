from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from . models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(csrf_exempt, name='dispatch')
class StudentAPI(View):
    def get(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id', None)

        if id is not None:
            student = Student.objects.get(id = id)
            serializer = StudentSerializer(student)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type= 'application/json')
        
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type = 'application/json')
    
    
    
    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = StudentSerializer(data = pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'data created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type = 'application/json')
        json_error = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_error, content_type = 'application/json')
    

    
    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        student = Student.objects.get(id = id)

        # Complete update, requires all the data from frontend/client
        serializer = StudentSerializer(student, data = pythondata)

        # patrial update, all the data not required
        # serializer = StudentSerializer(student, data = pythondata, partial=True)

        if serializer.is_valid():
            serializer.save()
            res = {'msg':'data updated'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type = 'application/json')
        json_error = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_error, content_type = 'application/json')
    
    
    
    def delete(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        student = Student.objects.get(id = id)
        student.delete()
        res = {'msg':'data deleted'}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type = 'application/json')
