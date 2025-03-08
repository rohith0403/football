import type { Component } from 'solid-js';
import {Router, Route} from '@solidjs/router'
import styles from './App.module.css';

import Leagues from './routes/Leagues'
import Clubs from './routes/Clubs'
const App: Component = () => {
  return (
    <div class={styles.App}>
      <Router>
        <Route path="/leagues" component={Leagues} />
        <Route path="/clubs" component={Clubs} />
      </Router>
    </div>
  );
};

export default App;
