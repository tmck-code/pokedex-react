import * as React from 'react';
import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import ButtonBase from '@mui/material/ButtonBase';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2
import Modal from '@mui/material/Modal';
import Typography from '@mui/material/Typography';

import fetchCards from './CardAPI.js';

const style = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  "&:hover": {
    backgroundcolor: "red"
  }
};

// <Button  ={(e) => handleClick(card.image_url)}>#{card.number_in_set}</Button>
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
        <Card variant="outlined">
          <CardMedia component="img" image={require('./' + image)} alt="pokemon" />
        </Card>
      </Box>
    </Modal>
  );
};

export default function Cards(params) {
  const [data, setData] = useState([]);
  const [open, setOpen] = useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const [image, setCard] = useState(true);

  const card_set_code = params['card_set_code']
  console.log('card_set_code:', params['card_set_code'])

  const handleClick = (value) => {
    setCard(value);
    handleOpen();
    console.log(value, image, open);
  };

  useEffect(() => {
      fetchCards(card_set_code).then((data) => {
        setData(data);
      });
  }, [])

  const listCards = data.map((card) => (
    <Grid key={"grid-"+card.number_in_set+"-"+card.title}>
      <ButtonBase
        key={"button-"+card.number_in_set+"-"+card.title}
        onClick={event => handleClick(card.image_url)}
      >
      <Box>
        <Card variant="outlined" sx={{ maxWidth: 300, maxHeight: 650 }}>
          <CardMedia
            component="img"
            image={require('./' + card.image_url)}
            alt={card.title}
            />
          <CardContent>
            <Typography variant="h5" component="div">#{card.number_in_set}: {card.title}</Typography>
          </CardContent>
        </Card>
      </Box>
      </ButtonBase>
    </Grid>
  ));

  return (
    <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
      {listCards}
      {open && CardModal(image, open, handleClose)}
    </Grid>
  );
}
