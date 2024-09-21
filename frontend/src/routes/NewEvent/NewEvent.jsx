import Navbar from "../../components/Navbar/Navbar"
import Footer from "../../components/Footer/Footer"
import "./newevent.css"

function NewEvent() {
  return (
    <>
      <Navbar />
      <div className="neweventpage">
        <header><h1>Host a new event!</h1></header><br></br>
        <main className="centered-square">
          <form>
            <div className="pad-10">
              <label htmlFor="name">Event name:</label><br></br>
              <input className="inputbox" type="text" id="name" name="name"></input><br></br>
            </div>
            
            <div className="pad-10">
              <label htmlFor="description">Description:</label><br></br>
              <textarea className="inputbox" id="description" name="description"></textarea><br></br>
            </div>
            
            <div className="pad-10">
              <label htmlFor="location">Location:</label><br></br>
              <textarea className="inputbox" id="location" name="location"></textarea><br></br>
            </div>
            
            <div className="pad-10">
              <label htmlFor="skills">Required Skills (ctrl+left click)</label><br></br>
              <select className="selectbox" name="skills" id="skills" multiple>
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
            </div>
            
            <div className="pad-10">
              <label htmlFor="urgency">Urgency level</label><br></br>
              <select className="inputbox" name="urgency" id="urgency">
                <option value="1">!</option>
                <option value="2">!!!</option>
                <option value="3">!!!!!</option>
              </select><br></br>
            </div>
            
            <div className="pad-10">
              <label htmlFor="date">Event date:</label><br></br>
              <input className="inputbox" type="datetime-local"
                id="Test_DatetimeLocal"
                min="2015-01-01T00:00"
                max="2025-12-31T23:59"
                step="1"></input><br></br><br></br>
            </div>
            
            <input className="submit-button" type="submit" value="Submit" />
            <br></br>
          </form>
        </main>
      </div>
      <Footer />
    </>
  )
}

export default NewEvent
