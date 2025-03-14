import type { Component } from 'solid-js';
import styles from './App.module.css';

import Routes from './routes/Routes';

const App: Component = () => {
  return (
    <div class={styles.App}>
      {/* <a href='/leagues'>Leagues</a>
      <a href='/clubs'>Clubs</a>
      <a href='/players'>Players</a>
      <hr class={styles.separator} />
      <Routes/> */}

      <h1 class={styles.gameMenuTitle}>Football Sim</h1>
      <div class={styles.gameMenuButtons}>
        <button classList={{ [styles.gameMenuButton]: true, [styles.gameMenuContinue]: true }}>
          Continue
        </button>
        <button classList={{ [styles.gameMenuButton]: true, [styles.gameMenuNewGame]: true }}>
          New Game
        </button>
      </div>

    </div>

  );
}

export default App;
