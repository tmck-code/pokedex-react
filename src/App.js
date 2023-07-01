import * as React from 'react';
import './App.css';

import SearchAppBar from './AppBar.js';
import Cards from './CardGrid.js';

export default function MyApp() {
  return (
    <div>
      <SearchAppBar />
      <Cards />
    </div>
  );
}
