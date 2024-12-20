import './App.css';
import { useState } from "react";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

function App() {
  const [price, setPrice] = useState(0);
  const [values, setValues] = useState([]);

  // Improved changePriceValue to handle price correctly
  const changePriceValue = (e) => {
    const newPrice = e.target.value;
    setPrice(newPrice);  // Update price state
    console.log(newPrice);  // Logging updated price for debugging
  };

  // Improved handleButton to fix URL template literal
  const handleButton = () => {
    const url = `http://127.0.0.1:8000/by_price?price=${price}`;
    fetch(url, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((data) => setValues(data))  // Update values with fetched data
      .catch((error) => console.error("Error fetching data:", error));  // Error handling
  };

  return (
    <div className="App">
      <div id="filter">
        <TextField
          id="outlined-basic"
          label="Введите цену"
          variant="outlined"
          type="number"
          value={price}  // Bind the price state to the input value
          onChange={changePriceValue}
        />
        <span>Введите цену</span>
        <input 
          id="price-field"
          type="number" 
          value={price}  // Bind to price state as well
          onChange={changePriceValue}
        />
        <Button variant="contained" onClick={handleButton}>Применить</Button> {/* Use MUI Button for consistency */}
      </div>

      <div>
        <TextField id="outlined-basic" label="Outlined" variant="outlined" />
        <Button variant="contained" onClick={handleButton}>Применить</Button>
      </div>

      <div id="table">
        <div className="row header">
          <p>Название</p>
          <p>Описание</p>
        </div>

        {values.map((item, index) => (
          <div className="row" key={index}>
            <p>{item.name}</p>
            <p>{item.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
