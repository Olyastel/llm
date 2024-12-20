import './App.css';
import { useState } from "react";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

function App() {
  const [price, setPrice] = useState(0);
  const [values, setValues] = useState([]);

  const changePriceValue = (e) => {
    console.log(e.target.value);
  }
    

const handleButton = () => {
  const url = 'http://127.0.0.1:8000/by_price?price=${price}';
  fetch(url, {
    method: "GET",
  })
  .then((data) => data.json())
  .then((data) => setValues(data));
};

console.log(values);

  return (
    <div className="App">
      <div id = "filter">
        <TextField
        id = "outlined-basic"
        label="Введите цену"
        variant="outlined"
        type="number"
        onChange={changePriceValue}
        />
        <span>Введите цену</span>
        <input id = 'price-field' type = 'number' onChange={changePriceValue}/>
        <button onClick={handleButton}> Применить </button>
      </div>

      <div>
        <TextField id="outlined-basic" label="Outlined" variant="outlined" />
        <Button variant="contained" onClick={handleButton}> Применить </Button>
      </div>
      <div id="table">
        <div classname = "row header">
          <p>{Название}</p>
          <p>{Описание}</p>
        </div> 
        {values.map((item)=>{
          return(
            <div classname = "row">
              <p>{item.name}</p>
              <p>{item.description}</p>
            </div>
          )
        })}             
      </div>
    </div>
  );
}

export default App;
