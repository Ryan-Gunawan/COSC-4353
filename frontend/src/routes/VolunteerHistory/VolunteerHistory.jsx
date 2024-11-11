import React, { useState, useEffect } from 'react';
import Navbar from "../../components/Navbar/Navbar"
import Footer from "../../components/Footer/Footer"
import "./volunteerhistory.css"

function VolunteerHistory() {

    const [userInfo, setUserInfo] = useState([])
    useEffect(() => {
        fetch("http://localhost:5000/api/userprofile", {
            method: 'GET',
            credentials: 'include',
        })
            .then(response => {
                if (!response.ok) {
                    console.error('Unable to load history:', response.statusText);
                    return; // Exit the promise chain
                }
                return response.json();
            })
            .then(data => {
                setUserInfo(data);
            })
            .catch(error => console.error('Error:', error));
    }, []);


    const [volunteerJobs, setVolunteerJobs] = useState([])
    useEffect(() => {
        fetch("http://localhost:5000/api/volunteerhistory", {
            method: 'GET',
            credentials: 'include',
        })
            .then(response => {
                if (!response.ok) {
                    console.error('Unable to load history:', response.statusText);
                    return; // Exit the promise chain
                }
                return response.json();
            })
            .then(data => {
                setVolunteerJobs(data);
            })
            .catch(error => console.error('Error:', error));
    }, []);

    return (
        <div className="page-container">
            <Navbar />

            <main className="main-content">
                <div className="historypage">
                    <div className="left-col">
                        <h3>{userInfo.fullname}</h3>
                        <p> {userInfo.city}, {userInfo.state} </p>
                        <p> Amount of Volunteer done: {volunteerJobs.length}</p>
                    </div>

                    <div className="right-col">
                        <h2> Volunteer History </h2>
                        {volunteerJobs.length === 0 ?
                            (<p>This persion has no volunteer history.</p>) :
                            (volunteerJobs.map((job, index) => (
                                <div key={index} className="event-card">
                                    <h3>{job.name}</h3>
                                    <p><strong>Date:</strong> {job.date}</p>
                                    <p><strong>Description:</strong> {job.description}</p>
                                    <p><strong>Location:</strong> {job.location}</p>
                                    <p><strong>Urgency:</strong> {job.urgency}</p>
                                    <p><strong></strong></p>
                                </div>
                            ))
                            )}
                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
};

export default VolunteerHistory;
