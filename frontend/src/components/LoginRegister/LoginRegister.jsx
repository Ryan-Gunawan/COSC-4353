import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginRegister.css";
import { FaLock, FaEnvelope } from "react-icons/fa";

const LoginRegister = () => {
  const [action, setAction] = useState("");

  const registerLink = () => {
    setAction(" register");
  };

  const loginLink = () => {
    setAction(" login");
  };

  const [inputs, setInputs] = useState({
    email: "",
    password: "",
  });

  const navigate = useNavigate(); // initialize useNavigate to redirect on submit

  const handleRegisterSubmit = async (e) => {
    e.preventDefault(); // prevents page reloading

    try {
      const response = await fetch("http://localhost:5000/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputs),
      });

      const result = await response.json();
      if (response.status === 200) {
        alert(result.msg); // show success msg
        //alert("Registered successfully");
        navigate("/userprofile");
      }
      else {
        alert(result.msg) // show error msg
      }
    } catch (error) {
      alert("A register error has occurred");
    }
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault(); // prevents page reloading

    try {
      const response = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputs),
      });

      // Gets result from backend. If email and password are valid go to home otherwise send error msg
      const result = await response.json();
      if (result.success) {
        navigate("/home");
        alert("Login successful");
      } else {
        alert(result.msg);
      }
    } catch (error) {
      alert("A login error has occurred");
    }
  };

  return (
    <div className="loginRegisterComponent">
      <div className={`container${action}`}>
        <div className="form-box login">
          <form action="" onSubmit={handleLoginSubmit}>
            <h1>Login</h1>
            <div className="input-box">
              <input
                type="email"
                maxLength="254"
                placeholder="Email"
                value={inputs.email}
                onChange={(e) =>
                  setInputs({ ...inputs, email: e.target.value })
                }
                required
              />
              <FaEnvelope className="icon" />
            </div>
            <div className="input-box">
              <input
                type="password"
                maxLength="128"
                placeholder="Password"
                value={inputs.password}
                onChange={(e) =>
                  setInputs({ ...inputs, password: e.target.value })
                }
                required
              />
              <FaLock className="icon" />
            </div>

            <button type="submit">Log in</button>

            <div className="register-link">
              <p>
                Don&apos;t have an account?{" "}
                <a href="#" onClick={registerLink} className="signup">
                  Register
                </a>
              </p>
            </div>
          </form>
        </div>

        <div className="form-box register">
          <form action="" onSubmit={handleRegisterSubmit}>
            <h1>Register</h1>
            <div className="input-box">
              <input
                type="email"
                maxLength="254"
                placeholder="Email"
                value={inputs.email}
                onChange={(e) =>
                  setInputs({ ...inputs, email: e.target.value })
                }
                required
              />
              <FaEnvelope className="icon" />
            </div>
            <div className="input-box">
              <input
                type="password"
                maxLength="128"
                placeholder="Password"
                value={inputs.password}
                onChange={(e) =>
                  setInputs({ ...inputs, password: e.target.value })
                }
                required
              />
              <FaLock className="icon" />
            </div>

            <div className="terms">
              <p>By signing up, you agree to our Terms.</p>
            </div>

            <button type="submit">Register</button>

            <div className="register-link">
              <p>
                Already have an account?{" "}
                <a href="#" onClick={loginLink} className="signup">
                  Log In
                </a>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
export default LoginRegister;
