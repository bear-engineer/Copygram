import { createStore, combineReducers } from "redux";
import users from "./modules/users";

const reducre = combineReducers({
  users
});

let store = initialState => createStore(reducre);

export default store();
