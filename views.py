import joblib
import numpy as np
from django.shortcuts import render



def home(request):
    return render(request, 'form.html')



model = joblib.load('predictor/model.pkl')

scaler = joblib.load('predictor/scaler.pkl')

le_color = joblib.load('predictor/le_color.pkl')

le_texture = joblib.load('predictor/le_texture.pkl')

le_soil = joblib.load('predictor/le_soil.pkl')

le_label = joblib.load('predictor/le_label.pkl')



def predict(request):

    if request.method == 'POST':

        try:

            # INPUT VALUES

            length = float(request.POST['length'])

            width = float(request.POST['width'])

            color = le_color.transform([
                request.POST['color']
            ])[0]

            spots = 1 if request.POST['spots'] == 'Yes' else 0

            moisture = float(request.POST['moisture'])

            texture = le_texture.transform([
                request.POST['texture']
            ])[0]

            humidity = float(request.POST['humidity'])

            temp = float(request.POST['temp'])

            soil = le_soil.transform([
                request.POST['soil']
            ])[0]

            # FEATURE ENGINEERING

            leaf_area = length * width

            temp_humidity = temp * humidity

            # FINAL INPUT ARRAY

            data = np.array([[

                length,
                width,
                color,
                spots,
                moisture,
                texture,
                humidity,
                temp,
                soil,
                leaf_area,
                temp_humidity

            ]])

           

            data = scaler.transform(data)

          

            if (
                spots == 0 and
                moisture >= 60 and
                humidity >= 60 and
                temp <= 30
            ):

                final_result = "Healthy"

            elif (
                spots == 1 and
                moisture < 50 and
                humidity < 50 and
                temp > 32
            ):

                final_result = "Unhealthy"

            else:

                prediction = model.predict(data)[0]

                final_result = le_label.inverse_transform([
                    prediction
                ])[0]

          

            return render(request, 'result.html', {

                'prediction': final_result,

                'accuracy': '55% - 65%',

                'best_model': 'Random Forest'

            })

        except Exception as e:

            return render(request, 'result.html', {

                'error': str(e)

            })

    return render(request, 'form.html')