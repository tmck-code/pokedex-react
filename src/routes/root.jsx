import { useState, useEffect } from 'react';

import * as API from '../CardAPI';

export default function Root() {
  const [data, setData] = useState([]);

  useEffect(() => {
      API.fetchCardSets().then((data) => {
        setData(data);
      });
  }, [])

  console.log('data', data)
  const listCardSets = data.map((card_set) => (
    <li> <a href={card_set.name + `/`}>{card_set.name}</a> </li>
  ));

  return (
    <>
      <div id="sidebar">
        <h1>tmck-code/pokedex-react</h1>
        <nav><ul>{listCardSets}</ul></nav>
      </div>
      <div id="detail"></div>
    </>
  );
}
