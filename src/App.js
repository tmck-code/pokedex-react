import * as React from 'react';
import {useState, useEffect} from 'react';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';


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
  // <img className="avatar" src={require('./' + card.image_url)} alt="logo" />
  // <!-- the max width of any pokemon image is 592 -->
  const listCards = data.map((card) =>
    <Grid>
      <Box>
        <Card variant="outlined" sx={{ maxWidth: 300, height: 650 }}>
          <CardMedia
            component="img"
            image={require('./' + card.image_url)}
            alt={card.title}
          />
          <CardContent>
            <Typography variant="body1" color="text.secondary" component="div">
	      #{card.number_in_set}
            </Typography>
            <Typography variant="h4" component="div">
              {card.title}
            </Typography>
          </CardContent>
        </Card>
      </Box>
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
    </div>
  );
}
