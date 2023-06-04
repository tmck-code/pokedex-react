import * as React from 'react';
import {useState, useEffect} from 'react';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
// for the zoom
import Switch from '@mui/material/Switch';
import Paper from '@mui/material/Paper';
import Zoom from '@mui/material/Zoom';
import FormControlLabel from '@mui/material/FormControlLabel';
import { Theme } from '@mui/material/styles';


import './App.css';


function Cards() {
  const [data, setData] = useState([])
  const [checked, setChecked] = React.useState(false);

  const fetchData = async ()=>{
    let res = await fetch('http://localhost:8000/cards/')
    let data = await res.json()
    console.log('response', data)
    setData(data)
  }

  useEffect(() => {
      fetchData()
  }, [])

  const handleChange = () => {
    setChecked((prev) => !prev);
  };

  const listCards = data.map((card) =>
  <Grid>

      <Box sx={{ height: 180 }}>
        <FormControlLabel
          control={<Switch checked={checked} onChange={handleChange} />}
          label="Show"
          />
        <Box sx={{ display: 'flex' }}>
          <Zoom in={checked}>
            <Box>
              {/* <!-- the max width of any pokemon image is 592 --> */}
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
          </Zoom>
        </Box>
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
