import { useState, useEffect } from 'react';

export default function Root() {

  const [data, setData] = useState([]);
  const fetchData = async ()=>{
    let res = await fetch('http://localhost:8000/card_sets/')
    let response = await res.json()
    console.log('response', response)
    setData(response)
  }

  useEffect(() => {
      fetchData()
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
