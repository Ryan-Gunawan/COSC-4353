import { useState } from "react";
import Navbar from "../../components/Navbar/Navbar"
import './NotificationsPage.css'
import NotificationGrid from "../../components/NotificationGrid/NotificationGrid";

function NotificationsPage() {



  return (
    <>
      <header>
        <Navbar />
        <h1 className="NotificationsHeader">Notifications</h1>
      </header>

      <div className="NotificationDiv">
        <NotificationGrid />
      </div>
    </>
  )
}
export default NotificationsPage
