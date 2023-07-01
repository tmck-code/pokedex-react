import * as React from 'react';
import './App.css';

import SearchAppBar from './AppBar.js';
import Cards from './CardGrid.js';

import {
Routes, Route, Link, BrowserRouter as Router
} from "react-router-dom";

export default function MyApp() {
  console.log('CardGrid');
  return (
    <div>
      <SearchAppBar />
      <Cards />
    </div>
  );
}
