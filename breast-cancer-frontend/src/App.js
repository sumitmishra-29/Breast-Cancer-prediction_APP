import React, { useState, useEffect } from 'react';
import './App.css';


// //const PredictionComponent = () => {
//   // State to store the result of the API call or any other data
//   const [result, setResult] = useState(null);

//   // This useEffect will run once when the component is mounted
//   useEffect(() => {
//       console.log("Component mounted");
//   }, []); // Empty dependency array means this runs only once when the component mounts

//   // This useEffect can be used to simulate data fetching or making an API call
//   useEffect(() => {
//       // Simulate API call or data fetch
//       setTimeout(() => {
//           setResult('Some Data'); // Setting the result after a simulated delay
//       }, 1000); // Simulated delay of 1 second
//   }, []); // Also runs only once when the component mounts

//   return (
//       <div>
//           <h1>Prediction Result:</h1>
//           {/* Check if result is available, if not show loading */}
//           {result ? <p>{result}</p> : <p>Loading...</p>}
//       </div>
//   );
// };

// export default PredictionComponent;

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

  useEffect(() => {
    console.log("Component mounted");
  }, []); 

  // Handle input change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Handle form submit to make the prediction request
  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })
      .then((response) => response.json())
      .then(data => {
        console.log(data); // Log the response from the server
        setResult(data.prediction); // Assuming your API returns a field 'prediction'
      })  // Check if data is being logged
      .catch(error => console.error('Error:', error));
  };

  return (
    <div className="App">
      <h1>Breast Cancer Diagnosis Prediction</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Radius Mean:</label>
          <input
            type="text"
            name="radius_mean"
            value={formData.radius_mean}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Perimeter Mean:</label>
          <input
            type="text"
            name="perimeter_mean"
            value={formData.perimeter_mean}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Area Mean:</label>
          <input
            type="text"
            name="area_mean"
            value={formData.area_mean}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Compactness Mean:</label>
          <input
            type="text"
            name="compactness_mean"
            value={formData.compactness_mean}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Concave Points Mean:</label>
          <input
            type="text"
            name="concave_points_mean"
            value={formData.concave_points_mean}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Area Worst:</label>
          <input
            type="text"
            name="area_worst"
            value={formData.area_worst}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Predict Diagnosis</button>
      </form>

      {result && (
        <div className="result">
          <h2>Prediction Result: {result}</h2>
        </div>
      )}
    </div>
  );
}

export default App;
