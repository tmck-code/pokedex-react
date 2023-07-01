export default function Root() {
  return (
    <>
      <div id="sidebar">
	<h1>tmck-code/pokedex-react</h1>
        <nav>
          <ul>
            <li> <a href={`/SV2A/`}>SV2A</a> </li>
            <li> <a href={`/SV1V/`}>SV1V</a> </li>
          </ul>
        </nav>
      </div>
      <div id="detail"></div>
    </>
  );
}
