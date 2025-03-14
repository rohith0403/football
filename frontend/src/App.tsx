import type { Component } from 'solid-js';
import styles from './App.module.css';

import Routes from './routes/Routes';
import GameMenu from './components/GameMenu'

const App: Component = () => {
  return (
    <div class={styles.App}>
      {/* <a href='/leagues'>Leagues</a>
      <a href='/clubs'>Clubs</a>
      <a href='/players'>Players</a>
      <hr class={styles.separator} />
      <Routes/> */}
      <GameMenu />
    </div>

  );
}

export default App;
