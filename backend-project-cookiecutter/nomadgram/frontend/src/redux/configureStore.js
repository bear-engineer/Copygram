import { combineReducers, createStore, applyMiddleware, compose } from "redux";
import { connectRouter, routerMiddleware } from "connected-react-router";
import createHistory from "history/createBrowserHistory";
import thunk from "redux-thunk";
import users from "redux/modules/users";

const env = process.env.NODE_ENV;

const history = createHistory();

const middlewares = [thunk, routerMiddleware(history)];

if (env === "development") {
  const { logger } = require("redux-logger");
  middlewares.push(logger);
}

const reducer = combineReducers({
  users,
  router: connectRouter(history)
});

let store = initialState =>
  createStore(
    connectRouter(history)(reducer),
    compose(applyMiddleware(...middlewares))
  );

export { history };

export default store();
