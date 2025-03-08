import type { Component } from 'solid-js';
import { Router, Route } from '@solidjs/router';
import styles from './App.module.css';

import Leagues from './routes/Leagues';
import Clubs from './routes/Clubs';
import Players from './routes/Players';

const App: Component = () => {
  return (
    <div class={styles.App}>
      <a href='/leagues'>Leagues</a>
      <a href='/clubs'>Clubs</a>
      <a href='/players'>Players</a>
      <hr class={styles.separator} />
      <Router>
        <Route path="/leagues" component={Leagues} />
        <Route path="/clubs" component={Clubs} />
        <Route path="players" component={Players} />
      </Router>
    </div>

  );
}

export default App;
