import LoginRegister from "../components/LoginRegister/LoginRegister"

// we'll need this for deployment. Not 100% sure if it goes here though.
// It'll need to be imported from here whenever we use it.
export const BASE_URL = import.meta.env.MODE === "development" ? "http://127.0.0.1:5000/api" : "/api";

function LoginRegisterPage() {

  return (
    <>
      <LoginRegister />
    </>
  )
}
export default LoginRegisterPage
