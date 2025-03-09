import { Router, Route } from '@solidjs/router';
import { createContext, useContext, createResource, Component, JSX, ParentComponent } from "solid-js";
import { createStore } from "solid-js/store";

import Leagues from './Leagues';
import Clubs from './Clubs';
import Players from './Players';

const Routes: Component = () => {
  return (
      <Router>
        <Route path="/leagues" component={Leagues} />
        <Route path="/clubs" component={Clubs} />
        <Route path="players" component={Players} />
      </Router>
  );
}

export default Routes;
