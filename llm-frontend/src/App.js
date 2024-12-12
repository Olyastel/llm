import './App.css';
import { useState } from "react";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

function App() {
  const [price, setPrice] = useState(0);

  const changePriceValue = (e) => {
    console.log(e.target.value);
  };

const handleButton = () => {
  console.log(price);};

  return (
    <div className="App">
      <div>
        <span>Введите цену</span>
        <input id = 'price-field' type = 'number' onChange={changePriceValue}/>
        <button onClick={handleButton}> Применить </button>
      </div>

      <div>
        <TextField id="outlined-basic" label="Outlined" variant="outlined" />
        <Button variant="contained" onClick={handleButton}> Применить </Button>
      </div>
    </div>
  );
}

export default App;
