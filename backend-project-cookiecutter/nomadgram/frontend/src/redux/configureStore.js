import { combineReducers, createStore, applyMiddleware, compose } from "redux";
import { connectRouter, routerMiddleware } from "connected-react-router";
import createHistory from "history/createBrowserHistory";
import thunk from "redux-thunk";
import users from "redux/modules/users";
import Reactotron from "ReactotronConfig";

const env = process.env.NODE_ENV;

const history = createHistory();

const middlewares = [thunk, routerMiddleware(history)];

if (env === "development") {
  const { logger } = require("redux-logger");
  middlewares.push(logger);
}

let store;

if (env === "development") {
  store = initialState =>
    Reactotron.createStore(
      connectRouter(history)(reducer),
      compose(applyMiddleware(...middlewares))
    );
} else {
  store = initialState =>
    createStore(
      connectRouter(history)(reducer),
      compose(applyMiddleware(...middlewares))
    );
}

const reducer = combineReducers({
  users,
  router: connectRouter(history)
});

export { history };

export default store();
