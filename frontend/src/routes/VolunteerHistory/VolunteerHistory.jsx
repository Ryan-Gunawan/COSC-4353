import Navbar from "../../components/Navbar/Navbar"
import Footer from "../../components/Footer/Footer"
import "./volunteerhistory.css"

function VolunteerHistory() {

  const userInfo = {
    fullName: "Elon Musk",
    city: "Houston",
    state: "TX",
    volunteerDone: 3,
  };

  const volunteerJobs = [
    {
      eventName: "Tech Conference 2024",
      description: "Join us for a day of insightful talks and networking with industry leaders in technology.",
      location: "San Francisco, CA",
      skills: ["Teamwork", "Detail Oriented"],
      urgency: "High",
      eventDate: "2024-10-15",
      eventStatus: "On-going",
    },
    {
      eventName: "Music Festival",
      description: "A weekend filled with live music performances from top artists around the world.",
      location: "Austin, TX",
      skills: ["Patience", "Communication"],
      urgency: "Low",
      eventDate: "2024-09-25",
      eventStatus: "Completed",
    },
    {
      eventName: "Startup Pitch Night",
      description: "Watch innovative startups pitch their ideas to investors and compete for prizes.",
      location: "New York, NY",
      skills: ["Leadership", "Teamwork", "Confidence"],
      urgency: "Intermediate",
      eventDate: "2024-11-05",
      eventStatus: "On-going",
    }];

  return (
    <div className="page-container">
      <Navbar />

      <main className="main-content">
        <div className="historypage">
          <div className="left-col">
            <h3>{userInfo.fullName}</h3>
            <p> {userInfo.city}, {userInfo.state} </p>
            <p> Amount of Volunteer done: {userInfo.volunteerDone}</p>
          </div>
          <div className="right-col">
            <h2> Volunteer History </h2>
            {volunteerJobs.map((job, index) => (
              <div key={index} className="event-card">
                <h3>{job.eventName}</h3>
                <p><strong>Date:</strong> {job.eventDate}</p>
                <p><strong>Description:</strong> {job.description}</p>
                <p><strong>Location:</strong> {job.location}</p>
                <p><strong>Required Skills:</strong> {job.skills.join(", ")}</p>
                <p><strong>Urgency:</strong> {job.urgency}</p>
                <p><strong>Status:</strong> {job.eventStatus} </p>
                <p><strong></strong></p>
              </div>
            ))}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default VolunteerHistory;
