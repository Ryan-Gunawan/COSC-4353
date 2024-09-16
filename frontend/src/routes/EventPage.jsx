import EventMatch from './EventMatch.jsx';

function EventPage() {

const router = createBrowserRouter([
  {
    path: "eventmatch",
    element: <EventMatch />,
  }
]);

  return (
    <>
      <header><h1>Events</h1></header>
      <h2>List of Events by Area</h2>
      <p><a href="">Cypress</a></p>
      <p><a href="">Houston downtown area</a></p>
      <p><a href="">Katy</a></p>
      <p><a href="">League City</a></p>
      <p><a href="">Pearland</a></p>
      <p><a href="">Sugarland</a></p>
      <p><a href="">Woodland</a></p>
    </>
  )
}
export default EventPage
