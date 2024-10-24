import React, { useState } from 'react';
import './App.css';
import logo from './logoapp.png';  // Import the logo
import awarenessImage from './awar.png';  // Import a real image

function App() {
  const [formData, setFormData] = useState({
    radius_mean: '',
    perimeter_mean: '',
    area_mean: '',
    compactness_mean: '',
    concave_points_mean: '',
    area_worst: ''
  });
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
    
      .then((response) => response.json())
      .then((data) => {
        if (data.prediction === 1) {
          setResult("Malignant (Cancer found, take doctor's prescription)");
        } else {
          setResult("Benign (Not cancer, just an unusual growth of tissue)");
        }
      })
      .catch((error) => console.error('Error:', error));
  };

  return (
    <div className="App">
      {/* Awareness Section */}
      <div className="awareness-section">
        <img src={awarenessImage} alt="Breast Cancer Awareness" className="awareness-image" />
        <div className="awareness-text">
          <h2>Breast Cancer Awareness</h2>
          <p>Breast cancer is one of the most common cancers in women. Early detection can save lives. Make sure to schedule regular checkups and perform self-examinations.</p>
          <p>Breast cancer awareness isn't just about wearing pink; it's about understanding the journey, sharing the stories, and supporting the warriors. Early detection saves lives, and being informed can empower us all. By spreading awareness and encouraging regular check-ups, we stand together against this formidable opponent. Let's honor the fighters, survivors, and loved ones we've lost, and commit to a future where every ribbon represents not just hope, but triumph</p>
          <p>Stay informed, spread awareness, and take charge of your health!</p>
        </div>
      </div>

      {/* Form Section */}
      <div className="form-container">
        <header className="App-header">
          <img src={logo} alt="Breast Cancer AI Prediction" className="App-logo" />
          <h1>AI-Based Breast Cancer Diagnosis</h1>
          <p>Instant predictions based on your medical data.</p>
        </header>

        <form onSubmit={handleSubmit} className="prediction-form">
          <div className="form-group">
            <label>Radius Mean:</label>
            <input
              type="text"
              name="radius_mean"
              value={formData.radius_mean}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Perimeter Mean:</label>
            <input
              type="text"
              name="perimeter_mean"
              value={formData.perimeter_mean}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Area Mean:</label>
            <input
              type="text"
              name="area_mean"
              value={formData.area_mean}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Compactness Mean:</label>
            <input
              type="text"
              name="compactness_mean"
              value={formData.compactness_mean}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Concave Points Mean:</label>
            <input
              type="text"
              name="concave_points_mean"
              value={formData.concave_points_mean}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Area Worst:</label>
            <input
              type="text"
              name="area_worst"
              value={formData.area_worst}
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit" className="submit-button">Predict Diagnosis</button>
        </form>

        {result && (
          <div className={`result ${result.includes("Malignant") ? "malignant" : "benign"}`}>
            <h2>Prediction Result:</h2>
            <p>{result}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
