import './App.css';
import downloadIcon from './download-icon.png';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>MealGPT</h1>
        <p className="instructions">
          Enter your ingredients (separated by spaces or commas), a cuisine, and any dietary restrictions (e.g., vegetarian)
        </p>
        <form className="meal-form">
          <input type="text" placeholder="ingredients" className="input-field" required/>
          <input type="text" placeholder="cuisine (optional)" className="input-field" />
          <input type="text" placeholder="dietary restrictions (optional)" className="input-field" />
          <button type="submit" className="generate-button">
            Generate
          </button>
        </form>
        <p className="download-instruction">
          Download your recipe here!{' '}
        <img className="download-icon" src={downloadIcon} alt="Download" />
        </p>
      </header>
    </div>
  );
}

export default App;
