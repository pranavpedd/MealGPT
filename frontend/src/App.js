import React, { useState } from 'react';
import axios from 'axios';
import downloadLogo from './download-icon.png';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    ingredients: '',
    cuisine: '',
    restriction: '',
  });

  const [downloadLink, setDownloadLink] = useState(null);
  const [recipeTitle, setRecipeTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [recipeGenerated, setRecipeGenerated] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form data:', formData);
    setLoading(true);
    setDownloadLink(null);
    try {
      const generateResponse = await axios.post('http://127.0.0.1:5000/generate-recipe', formData);
      if (generateResponse.status === 201) {
        const filename = generateResponse.data.filename;
        const recipeTitle = filename.replace('.pdf', '');
        const response = await axios.get(
          `http://127.0.0.1:5000/download-recipe?filename=${filename}`,
          {
            responseType: 'blob',
          }
        );
        const url = window.URL.createObjectURL(
          new Blob([response.data], { type: 'application/pdf' })
        );
        setDownloadLink({ url, filename });
        setRecipeTitle(recipeTitle);
        setRecipeGenerated(true);
      } else {
        console.error('Failed to generate the recipe.');
      }
    } catch (error) {
      console.error('There was an error!', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFormData({
      ingredients: '',
      cuisine: '',
      restriction: '',
    });
    setDownloadLink(null);
    setRecipeGenerated(false);
    setRecipeTitle('');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>MealGPT</h1>
        <p className="instructions">
          Enter your ingredients (separated by spaces or commas), a cuisine, and any dietary
          restrictions (e.g., vegetarian)
        </p>
        <form className="meal-form" onSubmit={handleSubmit}>
          <input
            type="text"
            name="ingredients"
            placeholder="ingredients"
            className="input-field"
            value={formData.ingredients}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="cuisine"
            placeholder="cuisine (optional)"
            className="input-field"
            value={formData.cuisine}
            onChange={handleChange}
          />
          <input
            type="text"
            name="restriction"
            placeholder="dietary restrictions (optional)"
            className="input-field"
            value={formData.restriction}
            onChange={handleChange}
          />
          <div className="button-group">
            <button type="submit" className="generate-button">
              Generate
            </button>
            {recipeGenerated && (
              <button type="button" className="generate-button" onClick={handleClear}>
                Clear
              </button>
            )}
          </div>
        </form>
        {loading ? (
          <p className="loading-message">Loading...</p>
        ) : (
          downloadLink && (
            <>
              <p className="recipe-title">Here is your recipe: {recipeTitle}</p>
              <p className="download-instruction">
                Download your recipe here!{' '}
                <a
                  href={downloadLink.url}
                  download={downloadLink.filename}
                  target="_blank"
                  rel="noopener noreferrer">
                  <img className="download-icon" src={downloadLogo} alt="Download" />
                </a>
              </p>
            </>
          )
        )}
      </header>
      <div id="footer">
        <footer>
          <p id="copyright">© 2023 Pranav Peddamalla</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
