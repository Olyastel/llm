import './App.css'; 
import { useState } from "react";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

function App() {
  const [price, setPrice] = useState(0);
  const [values, setValues] = useState([]);

  const changePriceValue = (e) => {
    setPrice(e.target.value); 
  };

  const handleButton = () => {
    const url = `http://127.0.0.1:8000/by_price?price=${price}`;
    fetch(url, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((data) => setValues(data))  
      .catch((error) => console.error("Error fetching data:", error));
  };

  return (
    <div className="App">
      <div id="filter">
        <h1>Введите цену</h1>  {/* Title */}
        <TextField
          id="price-input"
          label="Введите цену"
          variant="outlined"
          type="number"
          value={price}
          onChange={changePriceValue}
          fullWidth
        />
        <Button
          variant="contained"
          onClick={handleButton}
          fullWidth
          style={{ marginTop: '20px' }}
        >
          Применить
        </Button>
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
