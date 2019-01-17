import React from "react";
import styles from "./styles.scss";
import Footer from "components/Footer";
import { Route, Switch } from "react-router-dom";

const App = props => [
  props.isLoggedIn ? <PrivateRoute key={2} /> : <PublicRoutes key={3} />,
  <Footer key={4} />
];

const PrivateRoute = props => (
  <Switch>
    <Route exact path="/" render={() => "feed"} />
    <Route exact path="/explore" render={() => "explore"} />
  </Switch>
);

const PublicRoutes = props => (
  <Switch>
    <Route exact path="/" render={() => "login"} />
    <Route exact path="/forgot" render={() => "password"} />
  </Switch>
);

export default App;
