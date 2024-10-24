from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
import numpy  as np
import pickle

# Initialize Flask app
app = Flask(__name__)
@app.route('/')
def home():
    return "Hello, Heroku!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    
CORS(app)
# Load the pre-trained model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
    # Load the pre-trained model
model = joblib.load('model.pkl')
print(model.feature_names_in_)

# Define a route to make predictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Create a DataFrame with the correct feature names
    feature_names = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 
                     'smoothness_mean', 'compactness_mean', 'concavity_mean', 
                     'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean']
    
    # Ensure the input matches the model's feature names
    features = pd.DataFrame([data], columns=feature_names)

    # Make the prediction
    prediction = model.predict(features)

    if prediction ==1:
        result = "Malignant (cancer found, take doctor's prescription)"
    else:
        result = "Benign (not cancer, just an unusual growth of tissue)"

    return jsonify({'prediction': str(result)})

    # # Get data from the request
    # data = request.get_json(force=True)

    # # Extract features from the data
    # # features = pd.DataFrame({
    # #     'radius_mean': [data['radius_mean']],
    # #     'perimeter_mean': [data['perimeter_mean']],
    # #     'area_mean': [data['area_mean']],
    # #     'compactness_mean': [data['compactness_mean']],
    # #     'concave points_mean': [data['concave_points_mean']],
    # #     'area_worst': [data['area_worst']]
    # # })
    # features = pd.DataFrame([data])
    # features = [data.get('radius_mean'), data.get('texture_mean'), data.get('perimeter_mean'),
    #             data.get('area_mean'), data.get('smoothness_mean'), data.get('compactness_mean'),
    #             data.get('concavity_mean'), data.get('concave points_mean'), data.get('symmetry_mean'),
    #             data.get('fractal_dimension_mean')]
    
    # #print(features.shape)
    # # features.rename(columns={
    # #     'area_worst': 'area worst',  # Fix name to match training
    # #     'concave_points_mean': 'concave points_mean'  # Fix name to match training
    # # }, inplace=True)


    # expected_features = [
    #     'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    #     'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean',
    #     'fractal_dimension_mean', 'radius_worst', 'texture_worst', 'perimeter_worst',
    #     'area worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst',
    #     'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'
    # ]
    # features.columns = [col.replace(' ', '_') for col in features.columns] 
    # features.rename(columns={
    #     'area worst': 'area_worst',
    #     'compactness worst': 'compactness_worst',
    #     'concave points_worst': 'concave points_worst',
    #     # Add more mappings here if needed...
    # }, inplace=True)

    # for feature in expected_features:
    #     if feature not in features.columns:
    #         features[feature] = 0  # or any default value like mean, if you prefer
    
    # # features = np.array([features])
    # # Make prediction using the model
    # prediction = model.predict(features)

    # # Return the prediction as a response
    # result = 'Malignant (Cancer Found)' if prediction[0] == 1 else 'Benign (No Cancer)'
    # return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
