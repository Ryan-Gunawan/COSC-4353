import React, { useState, useEffect } from 'react';
import Navbar from "../../components/Navbar/Navbar"
import Footer from "../../components/Footer/Footer"
import "./volunteerhistory.css"
import "../../../../backend/dummy/history.json"

function VolunteerHistory() {
  const userInfo = {
    fullName: "Elon Musk",
    city: "Houston",
    state: "TX",
    volunteerDone: 3,
  };

  const [volunteerJobs, setVolunteerJobs] = useState([])
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/volunteerHistory');
        const data = await response.json();
        setVolunteerJobs(data);
      } catch (error) {
        console.error("Error fetching:", error);
      }
    };
    fetchHistory();
  }, []);

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
