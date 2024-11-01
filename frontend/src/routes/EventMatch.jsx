import React, { useState, useEffect } from 'react';
import Navbar from "../components/Navbar/Navbar";
import Footer from '../components/Footer/Footer';

const PeopleEventMatcher = () => {
  const [people, setPeople] = useState([]);
  const [events, setEvents] = useState([]);
  const [selectedUserEmail, setSelectedUserEmail] = useState('');
  const [selectedEvent, setSelectedEvent] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/eventlist")
      .then((response) => response.json())
      .then((data) => setEvents(data))
      .catch((error) => console.error("Error fetching events:", error));

    fetch("http://127.0.0.1:5000/api/users")
      .then((response) => response.json())
      .then((data) => setPeople(data))
      .catch((error) => console.error("Error fetching users:", error));
  }, []);

  const handleUserSelect = (email) => setSelectedUserEmail(email);
  const handleEventSelect = (eventId) => setSelectedEvent(events.find(event => event.id === eventId));

  const handleConfirm = async () => {
    if (!selectedEvent) return alert("Please select an event");
    const person = people.find(p => p.email === selectedUserEmail);
    if (!person) return alert("No user selected for event");

    const userId = person.id;
    const eventId = selectedEvent.id;

    try {
      const response = await fetch('http://127.0.0.1:5000/api/match_user', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId, event_id: eventId }),
      });

      const updateResult = await response.json();
      if (response.ok) {
        console.log(updateResult.msg);
      } else {
        alert(updateResult.msg);
      }

      const notificationData = {
        userId: person.id,
        eventName: selectedEvent.name,
        eventDate: selectedEvent.date,
      };

      const notificationResponse = await fetch('http://127.0.0.1:5000/api/send-assignment-notification', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(notificationData),
      });

      const result = await notificationResponse.json();
      alert(notificationResponse.ok ? "Volunteer successfully matched and notification sent." : result.msg);
    } catch (error) {
      console.error("Failed to send notification:", error);
      alert("An error occurred while sending the notification.");
    }
  };

  return (
    <div style={styles.container}>
      <Navbar />
      
      <div style={styles.content}>
        <h2 style={styles.header}>Event Matcher</h2>

        <div>
          <h3>Select a User</h3>
          <select style={styles.dropdown} onChange={(e) => handleUserSelect(e.target.value)}>
            <option value="">Select User</option>
            {people.map((user) => (
              <option key={user.id} value={user.email}>
                {user.fullname || user.email}
              </option>
            ))}
          </select>
        </div>

        <div>
          <h3>Select an Event</h3>
          <select style={styles.dropdown} onChange={(e) => handleEventSelect(Number(e.target.value))}>
            <option value="">Select Event</option>
            {events.map((event) => (
              <option key={event.id} value={event.id}>
                {event.name}
              </option>
            ))}
          </select>
        </div>

        <button style={styles.button} onClick={handleConfirm}>Confirm Match</button>

        <div>
          <h3>Event Details</h3>
          {selectedEvent && (
            <div style={styles.eventItem}>
              <p><strong>Name:</strong> {selectedEvent.name}</p>
              <p><strong>Date:</strong> {selectedEvent.date}</p>
              <p><strong>Location:</strong> {selectedEvent.location}</p>
              <p><strong>Description:</strong> {selectedEvent.description}</p>
              <p>
                <strong>Required Skills:</strong>{" "}
                {selectedEvent.skills && selectedEvent.skills.length > 0
                  ? selectedEvent.skills.join(", ")
                  : "No specific skills required"}
              </p>
            </div>
          )}
        </div>

        <div>
          <h3>User Details</h3>
          {selectedUserEmail && (
            <UserInfo user={people.find((u) => u.email === selectedUserEmail) || {}} />
          )}
        </div>
      </div>

      <Footer />
    </div>
  );
};

const UserInfo = ({ user }) => {
  const { fullname, email, admin, address1, city, state, zipcode, skills, availability } = user;
  return (
    <div className="user-info" style={styles.eventItem}>
      <p><strong>Name:</strong> {fullname || "Not provided"}</p>
      <p><strong>Email:</strong> {email}</p>
      <p><strong>Admin:</strong> {admin ? "Yes" : "No"}</p>
      <p><strong>Address:</strong> {address1 || "Not provided"}, {city || "Not provided"}, {state || "Not provided"} {zipcode || ""}</p>
      <p><strong>Skills:</strong> {skills && skills.length > 0 ? skills.join(", ") : "No skills available"}</p>
      <p><strong>Availability:</strong> {availability && availability.length > 0 ? availability.join(", ") : "No availability dates"}</p>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
  },
  content: {
    flex: 1,
    padding: '20px',
  },
  header: {
    backgroundColor: '#28a745',
    color: 'white',
    textAlign: 'center',
    padding: '20px 0',
    marginBottom: '20px',
    fontSize: '2em',
  },
  eventList: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
    padding: '0 20px',
    listStyle: 'none',
    margin: 0,
  },
  eventItem: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    transition: 'transform 0.2s',
    textAlign: 'left',
  },
  dropdown: {
    marginTop: '10px',
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  },
  button: {
    marginTop: '10px',
    padding: '10px',
    borderRadius: '5px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
  },
};

export default PeopleEventMatcher;
