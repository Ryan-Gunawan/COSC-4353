import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import debounce from "lodash.debounce";
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

  const [isSubmitDisabled, setIsSubmitDisabled] = useState(true);

  // Error state for invalid email input
  const [emailError, setEmailError] = useState("");

  // Error state for invalid login credentials
  const [loginError, setLoginError] = useState("");

  const navigate = useNavigate(); // initialize useNavigate to redirect on submit

  // Email validation helper function
  const validateEmail = (email) => {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
  }

  // Debounce the validation function
  const debouncedValidateEmail = useCallback(
    debounce((email) => {
      if (email !== "") {
        if (!validateEmail(email)) {
          setEmailError("Invalid email");
        } else {
          setEmailError("");
        }
      }
    }, 300),
    []
  );

  // Update email state and trigger debounced validation
  const handleEmailChange = (e) => {
    const email = e.target.value;
    setInputs((prevState) => ({ ...prevState, email }));
    debouncedValidateEmail(email);
  };

  const handlePasswordChange = (e) => {
    setInputs((prevState) => ({ ...prevState, password: e.target.value }));
  }

  useEffect(() => {
    const isEmailValid = validateEmail(inputs.email);
    const areInputsFilled = inputs.email !== "" && inputs.password !== "";

    if (!isEmailValid || !areInputsFilled || emailError) {
      setIsSubmitDisabled(true);
    } else {
      setIsSubmitDisabled(false);
    }
  }, [inputs, emailError]); // Check validation whenever inputs change

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
        credentials: 'include' //ensure cookies and sessions are sent
      });

      // Gets result from backend. If email and password are valid go to home otherwise send error msg
      const result = await response.json();
      if (result.success) {
        navigate("/home");
        // alert("Login successful");
      } else {
        setLoginError("Sorry, your email or password was incorrect. Please double-check and try again.")
        // alert(result.msg);
      }
    } catch (error) {
      setLoginError("An error occurred during login");
      // alert("A login error has occurred");
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
                // onChange={(e) =>
                //   setInputs({ ...inputs, email: e.target.value })
                // }
                onChange={handleEmailChange} // Debounced email change handler
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

            {loginError && <div className="error-text">{loginError}</div>}

            <button type="submit" disabled={isSubmitDisabled}>Log in</button>

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
                // onChange={(e) => {
                //   setInputs({ ...inputs, email: e.target.value });
                //   if (validateEmail(e.target.value)) {
                //     setEmailError("Invalid email input");
                //   } else {
                //     setEmailError("");
                //   }
                //   console.log("Email error:", emailError); // check if error updates
                // }}
                onChange={handleEmailChange} // Debounced email change handler
                className={emailError ? "input-error" : ""} // adds input error class if email is invalid
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
            {emailError && <p className="error-text">{emailError}</p>}

            <div className="terms">
              <p>By signing up, you agree to our Terms.</p>
            </div>

            <button type="submit" disabled={isSubmitDisabled}>Register</button>

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
