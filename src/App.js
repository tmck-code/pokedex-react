import * as React from 'react';
import './App.css';

import SearchAppBar from './AppBar.js';
import Cards from './CardGrid.js';

import { useParams } from 'react-router-dom';

/**
 * This is the main function of the app, it displays a grid of Pokemon cards and a simple App bar
 */
export default function MyApp() {
  let params = useParams();
  console.log(`[MyApp] entering main MyApp function, params: ${params}`);

  return (
    <div key={`MyApp`}>
      {/* This is the main control bar, which is always at the top of the page */}
      <SearchAppBar />

      {/* This is the grid of displayed Pokemon cards & metadata */}
      <Cards card_set_code={params['cardSetCode']}/>
    </div>
  );
}
