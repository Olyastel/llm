import './App.css';
import { useState } from "react";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

function App() {
  const [price, setPrice] = useState("");  
  const [values, setValues] = useState([]);  

  const changePriceValue = (e) => {
    setPrice(e.target.value);  
  };

  const handleButton = () => {
    if (!price) {  
      alert("Пожалуйста, введите цену.");
      return;
    }

    const url = `http://127.0.0.1:8000/llm_filtered?price=${price}`;
    fetch(url, {
      method: "GET", 
    })
      .then((response) => response.json()) 
      .then((data) => {
        if (Array.isArray(data)) {
          setValues(data); 
        } else {
          console.error('Полученные данные не являются массивом:', data);
        }
      })
      .catch((error) => console.error("Ошибка при получении данных:", error));
  };

  return (
    <div className="App">
      <div id="container">
        <div id="title">
          <h1>Фильтрация Chat gpt по цене</h1>
        </div>
        <div id="description">
          <p>Введите данные, чтобы отфильтровать товары, соответствующие вашему запросу</p>
        </div>
        <div id="filter">
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
            <p>Название товара</p>
            <p>Описание товара</p>
          </div>

          {values.length === 0 && <p>Нет результатов</p>}
          {values.map((item, index) => (
            <div className="row" key={index}>
              <p>{item.name}</p>
              <p>{item.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
