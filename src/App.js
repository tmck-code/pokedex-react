import * as React from 'react';
import './App.css';

import SearchAppBar from './AppBar.js';
import Cards from './CardGrid.js';

import { useParams } from 'react-router-dom';


export default function MyApp() { 
  console.log('CardGrid');
  let params = useParams();

  console.log('params:', params['cardSetCode']);
  
  return (
    <div>
      <SearchAppBar />
      <Cards card_set_code={params['cardSetCode']}/>
    </div>
  );
}
