import * as React from 'react'
import * as ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import './index.css'
import LoginRegisterPage from './routes/LoginRegisterPage.jsx';
import HomePage from './routes/HomePage/HomePage.jsx';
import EventPage from './routes/EventPage.jsx';
import NewEvent from './routes/NewEvent.jsx';
import EventList from './routes/EventList.jsx';
import EventMatch from './routes/EventMatch.jsx';
import NotificationsPage from './routes/NotificationsPage/NotificationsPage.jsx';
import UserProfile from './routes/UserProfile/UserProfile.jsx';

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
  {
    path: "event",
    element: <EventPage />,
  },
  {
    path: "newevent",
    element: <NewEvent />,
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
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
