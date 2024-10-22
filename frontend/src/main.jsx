import * as React from 'react'
import * as ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import './index.css'
import LoginRegisterPage from './routes/LoginRegisterPage.jsx';
import HomePage from './routes/HomePage/HomePage.jsx';
import NewEvent from './routes/NewEvent/NewEvent.jsx';
import SuccessPage from './routes/NewEvent/SuccessPage.jsx';
import EventList from './routes/EventList/EventList.jsx';
import EventMatch from './routes/EventMatch.jsx';
import NotificationsPage from './routes/NotificationsPage/NotificationsPage.jsx';
import UserProfile from './routes/UserProfile/UserProfile.jsx';
import VolunteerHistory from './routes/VolunteerHistory/VolunteerHistory.jsx';
// import SocketProvider from './SocketProvider.jsx';

const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginRegisterPage />,
  },
  {
    path: "home",
    element: <HomePage />,
  },
  {
    path: "newevent",
    element: <NewEvent />,
  },
  {
    path: "success",
    element: <SuccessPage />,
  },
  {
    path: "eventlist",
    element: <EventList />,
  },
  {
    path: "eventmatch",
    element: <EventMatch />,
  },
  {
    path: "notifications",
    element: <NotificationsPage />,
  },
  {
    path: "userprofile",
    element: <UserProfile />,
  },
  {
    path: "volunteerhistory",
    element: <VolunteerHistory />,
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
