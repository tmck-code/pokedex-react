import {useState, useCallback, useEffect} from 'react';
import './App.css';

function Cards() {
  const [data, setData] = useState([])

  const fetchData = async ()=>{
    let res = await fetch('http://localhost:8000/cards/')
    let data = await res.json()
    setData(data)
  }

  useEffect(() => {
      fetchData()
  }, [])

  const listCards = data.map((card) =>
    <li key={card.number_in_set}>
      <p>{JSON.stringify(card)}</p>
    </li>
  );

  return (
    <ul>{listCards}</ul>
  );
}

export default function MyApp() {
  return (
    <div>
      <Cards />
      <h1>Welcome to my app</h1>
    </div>
  );
}
