import * as React from 'react';
import {useState, useEffect} from 'react';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
// for the zoom
// import Switch from '@mui/material/Switch';
// import Paper from '@mui/material/Paper';
// import Zoom from '@mui/material/Zoom';
// import FormControlLabel from '@mui/material/FormControlLabel';
// import { Theme } from '@mui/material/styles';
// Modal
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';


import './App.css';


const style = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  "&:hover": {
    backgroundcolor: "red"
  }
};

function CardModal(image, open, handleClose) {
  return (
    <Modal
      sx={style}
      open={open}
      onClose={handleClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        {/* <!-- the max width of any pokemon image is 592 --> */}
        <Card variant="outlined" sx={{ maxWidth: 300, height: 650 }}>
          <CardMedia
            component="img"
            image={require('./' + image)}
            alt="pokemon"
          />
        </Card>
      </Box>
    </Modal>
  );
};

function Cards() {
  const [data, setData] = useState([]);
  const [open, setOpen] = useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const [image, setCard] = useState(true);

  const handleClick = (value) => {
    setCard(value);
    handleOpen();
    console.log(value, image, open);
  };


  const fetchData = async ()=>{
    let res = await fetch('http://localhost:8000/cards/')
    let data = await res.json()
    console.log('response', data)
    setData(data)
  }

  useEffect(() => {
      fetchData()
  }, [])

  const listCards = data.map((card) => (
    <Grid key={card.number_in_set}>
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
      <Button onClick={(e) => handleClick(card.image_url)}>#{card.number_in_set} {card.title}</Button>
    </Grid>
  ));

  return (
    <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
      {listCards}
      {open && CardModal(image, open, handleClose)}
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
