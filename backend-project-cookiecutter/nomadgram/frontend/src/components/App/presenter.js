import React from "react";
import PropTypes from "prop-types";
import "./styles.scss";
import Footer from "components/Footer";
import { Route, Switch } from "react-router-dom";
import Auth from "components/Auth";

const App = props => [
  props.isLoggedIn ? <PrivateRoute key={2} /> : <PublicRoutes key={3} />,
  <Footer key={4} />
];

App.propTypes = {
  isLoggedIn: PropTypes.bool.isRequired
};

const PrivateRoute = props => (
  <Switch>
    <Route exact path="/" render={() => "feed"} />
    <Route exact path="/explore" render={() => "explore"} />
  </Switch>
);

const PublicRoutes = props => (
  <Switch>
    <Route exact path="/" component={Auth} />
    <Route exact path="/forgot" render={() => "password"} />
  </Switch>
);

export default App;
