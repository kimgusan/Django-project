from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
import os.path
from pathlib import Path
import joblib
# from sklearn.linear_model import LogisticRegression
from rest_framework.response import Response
import numpy as np
from sklearn.preprocessing import Binarizer


class AiView(View):
    def get(self, request):
        return render(request, 'ai/index.html')


class AiAPIView(APIView):
    def post(self, request):
        datas = request.data
        datas = np.array(list(datas.values())).astype('float16')
        model = joblib.load(os.path.join(Path(__file__).resolve().parent, 'ai/machine.pkl'))
        binarizer = Binarizer(threshold=0.2968)
        custom_prediction = binarizer.fit_transform(model.predict_proba(datas.reshape(-1, 4))[:, 1].reshape(-1, 1))
        return Response(custom_prediction[0])
