# from django.shortcuts import render
# from multiprocessing import connection
# from django.db import connection
# from django.http import HttpResponse
# # Create your views here.
# from qc_form.models import QCForm


# def index(request):

#     posts = QcForm.objects.raw("SELECT * FROM form_qc_qcform")

#     print("A")
#     print(posts)
#     print(connection.queries)
#     return render(request, 'output.html',{'data':posts})
#     # return HttpResponse("Hello, world. You're at the polls index.")