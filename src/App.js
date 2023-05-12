import {useState, useEffect} from 'react';
import './App.css';

function Cards() {
  const [data, setData] = useState([])

  const fetchData = async ()=>{
    let res = await fetch('http://localhost:8000/cards/')
    let data = await res.json()
    console.log('response', data)
    setData(data)
  }

  useEffect(() => {
      fetchData()
  }, [])

  // <img src={`data:image/jpeg;base64,${card.image_url}`} alt="secret"/>
  const listCards = data.map((card) =>
    <li key={card.number_in_set}>
      <p>{card.title}</p>
      <p>{JSON.stringify(card)}</p>
      <img className="avatar" src={require('./' + card.image_url)} alt="logo" />
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
