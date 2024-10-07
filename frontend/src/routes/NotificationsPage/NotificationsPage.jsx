import Navbar from "../../components/Navbar/Navbar"
import './NotificationsPage.css'
import NotificationGrid from "../../components/NotificationGrid/NotificationGrid";
import Footer from ".././../components/Footer/Footer"

function NotificationsPage() {



  return (
    <>
      <div className="page-container">
        <header>
          <Navbar />
        </header>

        <main className="main-content">
          <h1 className="NotificationsHeader">Notifications</h1>
          <NotificationGrid />
        </main>

        <Footer />
      </div>
    </>
  )
}
export default NotificationsPage
