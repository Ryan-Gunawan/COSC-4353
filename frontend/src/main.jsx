import * as React from 'react'
import * as ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import './index.css'
import LoginRegisterPage from './routes/LoginRegisterPage.jsx';
import HomePage from './routes/HomePage.jsx';


const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginRegisterPage />,
  },
  {
    path: "home",
    element: <HomePage />,
  },
  // Add more routes here for any additional pages

]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
