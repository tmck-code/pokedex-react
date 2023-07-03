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

/**
 * The is the modal that pops up when a card is clicked, showing a larger image of the card
 */
function CardModal(card, handleClose) {
  console.log(`[CardModal] '${card}'`)
  return (
    <Modal
      sx={style}
      open={card !== false}
      onClose={handleClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        <Card variant="outlined">
          <CardMedia component="img" image={require('./' + card)} alt="pokemon" />
        </Card>
      </Box>
    </Modal>
  );
};

/**
 * This is the card grid that displays all the cards in the selected set,
 * and the modal that displays larger images of the cards.
*/
export default function Cards(params) {
  const [cards, setCards] = useState([]);
  const [modalCard, setModalCard] = useState(false);

  const handleModalClose = () => setModalCard(false);  
  const handleClick = (value) => setModalCard(value);

  const card_set_code = params['card_set_code']

  useEffect(() => {
    fetchCards(card_set_code).then((data) => {
      setCards(data);
    });
  }, [card_set_code])

  const listCards = cards.map((card) => (
    <Grid key={"grid-"+card.number_in_set+"-"+card.title}>
      <ButtonBase
        key={"button-"+card.number_in_set+"-"+card.title}
        onClick={(event) => handleClick(card.image_url)}
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
      {modalCard && CardModal(modalCard, handleModalClose)}
    </Grid>
  );
}
