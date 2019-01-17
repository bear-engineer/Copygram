import React from "react";
import Ionicon from "react-ionicons";
import "./styles.scss";

export const LoginForm = props => (
  <div>
    <form>
      <input type="text" placeholder="username" />
      <input type="password" placeholder="password" />
      <input type="submit" value="Login" />
    </form>
    <span>or</span>
    <span>
      <Ionicon icon="logo-facebook" fontSize="20px" color="#385185" />
      Login with Facebook
    </span>
    <span>Forgot password?</span>
  </div>
);

export const SignupForm = props => (
  <div>
    <h3>Sign up to see photos and viedos from your friends.</h3>
    <button>
      <Ionicon icon="logo-facebook" fontSize="20px" color="#fff" />
      Login with Facebook
    </button>
    <span>or</span>
    <form>
      <input type="email" placeholder="email" />
      <input type="text" placeholder="full name" />
      <input type="username" placeholder="username" />
      <input type="password" placeholder="password" />
      <input type="submit" value="Signup" />
    </form>

    <p>
      By signing up. you agree to our <span>Terms & Privacy Policy</span>.
    </p>
  </div>
);
