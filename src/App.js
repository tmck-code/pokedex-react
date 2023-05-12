import {useState, useEffect} from 'react';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2

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
  //  <li key={card.number_in_set}>
  //    <p>{card.title}</p>
  //    <p>{JSON.stringify(card)}</p>
  //  </li>
  const listCards = data.map((card) =>
    <Grid>
      <img className="avatar" src={require('./' + card.image_url)} alt="logo" />
      <p>{card.name}</p>
    </Grid>
  );

  return (
    <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
      {listCards}
    </Grid>
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
