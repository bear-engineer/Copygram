import { combineReducers, createStore, applyMiddleware, compose } from "redux";
import { connectRouter, routerMiddleware } from "connected-react-router";
import createHistory from "history/createBrowserHistory";
import thunk from "redux-thunk";
import user from "redux/modules/user";

import { composeWithDevTools } from "redux-devtools-extension";
import { i18nState } from "redux-i18n";
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
    createStore(
      connectRouter(history)(reducer),
      composeWithDevTools(applyMiddleware(...middlewares))
    );
} else {
  store = initialState =>
    createStore(
      connectRouter(history)(reducer),
      compose(applyMiddleware(...middlewares))
    );
}

const reducer = combineReducers({
  user,
  router: connectRouter(history),
  i18nState
});

export { history };

export default store();
