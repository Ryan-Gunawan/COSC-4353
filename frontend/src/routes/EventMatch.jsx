import React, { useState, useEffect } from 'react';
import Navbar from "../components/Navbar/Navbar";
import Footer from '../components/Footer/Footer';

const PeopleEventMatcher = () => {
  const [people, setPeople] = useState([]);
  const [events, setEvents] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState({});
  const [alertMessage, setAlertMessage] = useState('');

  useEffect(() => {
    // Fetch additional events from the database
    fetch("http://127.0.0.1:5000/api/eventlist")
      .then((response) => response.json())
      .then((data) => {
        const uniqueEvents = data.filter(
          (event, index, self) =>
            index === self.findIndex((e) => e.id === event.id)
        );
        setEvents(uniqueEvents);
      })
      .catch((error) => console.error('Error fetching events:', error));

    // Fetch users from the /api/userslist endpoint
    fetch("http://127.0.0.1:5000/api/users")
      .then((response) => response.json())
      .then((data) => setPeople(data))
      .catch((error) => console.error("Error fetching users:", error));
  }, []);

  // Handles confirm button press for matching a user to an event
  const handleConfirm = async (eventId) => {
    const selectedUserEmail = selectedUsers[eventId];
    if (!selectedUserEmail) {
      alert("No user selected for event");
      return;
    }

    const selectedUser = people.find(person => person.email === selectedUserEmail);
    if (!selectedUser) {
      alert("User not found");
      return;
    }

    // Send PUT request to match user to event
    const response = await fetch('http://127.0.0.1:5000/api/match_user', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: selectedUser.id, event_id: eventId })
    });

    const result = await response.json();
    if (response.ok) {
      alert(result.msg);
    } else {
      alert("Error: " + result.msg);
    }
  };


  return (
    <div>
      <Navbar />
      <h2 style={styles.header}>Event Matcher</h2>

      <div style={styles.eventList}>
        {events.map(event => (
          <div key={event.id} style={styles.eventBox}>
            <h3>{event.name}</h3>
            <p><strong>Date:</strong> {
              event.date ?
                new Date(event.date).toLocaleString('en-CA', {
                  year: 'numeric',
                  month: '2-digit',
                  day: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit',
                  second: '2-digit',
                  hour12: false,
                }).replace(',', '') : 'TBA'
            }</p>
            <p><strong>Location:</strong> {event.location}</p>
            <p><strong>Description:</strong> {event.description}</p>
            <p><strong>Skills Preferred:</strong> {
              event.skills ?
                JSON.parse(event.skills).join(', ') :
                'No specific skills required'
            }</p>

            <select
              style={styles.dropdown}
              onChange={(e) => setSelectedUsers(prev => ({ ...prev, [event.id]: e.target.value }))}
            >
              <option value="">Select User</option>
              {people.map(person => (
                <option key={person.id} value={person.email}>
                  {person.fullname || person.email}
                </option>
              ))}
            </select>
            <button style={styles.button} onClick={() => handleConfirm(event.id)}>
              Confirm Match
            </button>
          </div>
        ))}

        {alertMessage && <p>{alertMessage}</p>}
      </div>
      <Footer />
    </div>
  );
};

const styles = {
  header: {
    backgroundColor: '#28a745',
    color: 'white',
    textAlign: 'center',
    padding: '20px 0',
    marginBottom: '20px',
    fontSize: '2em',
  },
  generateReportContainer: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '20px auto',
    maxWidth: '400px',
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
  reportLabel: {
    marginRight: '10px',
    marginTop: '8px',
    fontWeight: 'bold',
    textAlign: 'center'
  },
  eventList: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
    padding: '20px',
  },
  eventBox: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    textAlign: 'left',
  },
  dropdown: {
    marginTop: '10px',
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc',
    width: '100%',
  },
  button: {
    marginTop: '10px',
    padding: '10px',
    borderRadius: '5px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
    width: '100%',
  },
};

export default PeopleEventMatcher;
