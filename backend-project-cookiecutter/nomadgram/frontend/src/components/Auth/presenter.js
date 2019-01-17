import React from "react";
import "./styles.scss";
import { LoginForm, SignupForm } from "components/AuthForms";

const Auth = (props, context) => (
  <main className="auth">
    <div className="column">
      <img src={require("images/phone.png")} alt="" />
    </div>
    <div className="column">
      <div className="white-box from-box">
        <img src={require("images/logo.png")} alt="logo" />
        {props.action === "login" && <LoginForm />}
        {props.action === "signup" && <SignupForm />}
      </div>
      <div className="white-box">
        {props.action === "login" && (
          <p>
            Don't have an account?{""}
            <span className="change-link" onClick={props.changeAction}>
              Sigh up
            </span>
          </p>
        )}
        {props.action === "signup" && (
          <p>
            Have an account?{" "}
            <span className="change-link" onClick={props.changeAction}>
              Sigh in
            </span>
          </p>
        )}
      </div>
      <div className="app-box">
        <span>Get the app</span>
        <div className="appstores">
          <img src={require("images/ios.png")} alt="" />
          <img src={require("images/android.png")} alt="" />
        </div>
      </div>
    </div>
  </main>
);

export default Auth;
