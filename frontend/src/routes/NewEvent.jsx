import EventMatch from "./EventMatch.jsx";

function NewEvent() {

  const router = createBrowserRouter([
  {
    path: "eventmatch",
    element: <EventMatch />,
  }
]);

  return (
    <>
      <header><h1>Host a new event!</h1></header><br></br>
      <form>
        <label htmlFor="name">Event name:</label><br></br>
        <input type="text" id="name" name="name"></input><br></br>
        <label htmlFor="description">Description:</label><br></br>
        <textarea id="description" name="description"></textarea><br></br>
        <label htmlFor="location">Location:</label><br></br>
        <textarea id="location" name="location"></textarea><br></br>
        <label htmlFor="skills">Required Skills (ctrl+left click)</label><br></br>
        <select name="skills" id="skills" multiple>
          <option value="organized">Organized</option>
          <option value="leadership">Leadership</option>
          <option value="goodwithchildren">Good with children</option>
          <option value="communication">Communication</option>
          <option value="problemsolver">Problem Solver</option>
          <option value="timemanagement">Time management</option>
          <option value="adaptability">Adaptability</option>
          <option value="teamwork">Teamwork</option>
          <option value="creativity">Creativity</option>
        </select><br></br>
        <label htmlFor="urgency">Urgency level</label><br></br>
        <select name="urgency" id="urgency">
          <option value="1">!</option>
          <option value="2">!!!</option>
          <option value="3">!!!!!</option>
        </select><br></br>
        <label htmlFor="date">Event date:</label><br></br>
        <input type="datetime-local" 
               id="Test_DatetimeLocal" 
               min="2015-01-01T00:00" 
               max="2025-12-31T23:59" 
               step="1"></input><br></br><br></br>
        <input type="submit" value="Submit" />
      </form>
    </>
  )
}

export default NewEvent
