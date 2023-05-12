import {useState, useCallback} from 'react';
import './App.css';

function MyButton() {
  const [data, setData] = useState({data: []});
  const [isLoading, setIsLoading] = useState(false);
  const [err, setErr] = useState('');

  const sendRequest = useCallback(async () => {
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/cards', {
        method: 'GET',
        headers: {
          Accept: 'application/json',
        },
	mode:'cors'
      });

      if (!response.ok) {
        throw new Error(`Error! status: ${response.status}`);
      }

      const result = await response.json();

      console.log('result is: ', JSON.stringify(result, null, 4));

      setData(result);
    } catch (err) {
      setErr(err.message);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]) // update the callback if the state changes

  return (
    <input type="button" onClick={sendRequest} />
  )

}

const cards = [
  {
    name: 'Erika\'s Hospitality',
    imageUrl: 'https://den-cards.pokellector.com/288/Erikas-Hospitality.SM12A.190.30530.png',
    imageSize: 90,
  }
];

function Cards() {
  const listItems = cards.map(card =>
    <li
      key={card.name}
      style={{
        color: true ? 'magenta' : 'darkgreen'
      }}
    >
      <i>{card.name}</i>
      <img
        className="avatar"
        src={card.imageUrl}
        alt={'Photo of ' + card.name}
        style={{
          width: card.imageSize,
          height: card.imageSize
        }}
      />
    </li>
  );

  return (
    <ul>{listItems}</ul>
  );
}

const handleClick = async () => {
}





export default function MyApp() {
  return (
    <div>
      <Cards />
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}
