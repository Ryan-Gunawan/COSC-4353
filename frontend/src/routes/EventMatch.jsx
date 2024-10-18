import React, { useState, useEffect } from 'react';
import Navbar from "../components/Navbar/Navbar";
import Footer from '../components/Footer/Footer';

const PeopleEventMatcher = () => {
  // State to store users, events, selected events, and alert message
  const [people, setPeople] = useState([]);
  const [events, setEvents] = useState([]);
  const [selectedEvents, setSelectedEvents] = useState({});
  const [alertMessage, setAlertMessage] = useState('');

  // Fetch the user list from userinfo.json
  useEffect(() => {
    const fetchUsers = async () => {
      const response = await fetch('http://127.0.0.1:5000/api/usersList');
      const usersData = await response.json();
      // Assuming usersData is structured as { users: [...] }
      setPeople(usersData.users);
    };

    fetchUsers();
  }, []);

  // Fetch the event list
  useEffect(() => {
    const fetchEvents = async () => {
      const eventsResponse = await fetch('http://127.0.0.1:5000/api/eventlist');
      const eventsData = await eventsResponse.json();
      setEvents(eventsData);
    };

    fetchEvents();
  }, []);

  const hasRequiredSkills = (personSkills, requiredSkills) => {

    personSkills = Array.isArray(personSkills) ? personSkills : [];
    requiredSkills = Array.isArray(requiredSkills) ? requiredSkills : [];

    if(requiredSkills.length === 0){
      return true;
    }
    
    // Normalize skills to lower case and trim whitespace
    const normalizedPersonSkills = personSkills.map(skill => skill.toLowerCase().trim());
    const normalizedRequiredSkills = requiredSkills.map(skill => skill.toLowerCase().trim());

    // Check if at least one required skill is in person's skills
    return normalizedRequiredSkills.some(skill => normalizedPersonSkills.includes(skill));
};

  // Function to check if the person is available for the event
  const isAvailable = (personAvailability, eventDate) => {
    personAvailability = Array.isArray(personAvailability) ? personAvailability : [];
    eventDate = Array.isArray(eventDate) ? eventDate : [];

    return true;
  };


  // Handles confirm button press
  const handleConfirm = async (eventName) => {

    const selectedEvent = events.find(event => event.name === eventName);
    const selectedUser = selectedEvents[eventName];
    // Ensure that a user is selected
    if (!selectedUser) {
        alert("No user selected for event");
        return;
    }
    // Find the selected user based on their email
    const person = people.find(p => p.email === selectedUser);
    if (!person) {
        alert("No user selected for event");
        return;
    }
    const userId = person.id;
    const eventId = selectedEvent.id;

    // Check if user has required skills
    if (!hasRequiredSkills(person.skills, selectedEvent.requiredSkills)) {
        alert("User does not have the required skills for this event.");
        return;
    }
    // Check if user has avaliability
    if (!isAvailable(person.availability, selectedEvent.date)) {
          alert("User is not avaliable for this event.");
          return;
      }

    // Send POST request to match user to event
    const response = await fetch('http://127.0.0.1:5000/api/match_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId, event_id: eventId }),
    });

    const responseData = await response.json();

    if (response.ok) {
        alert(responseData.message);
    } else {
        alert(responseData.message);
    }

    try {
      const notificationData = {
          userId: person.id, // Assuming the user's ID is available
          eventName: selectedEvent.name,
          eventDate: selectedEvent.date,
      };

      const response = await fetch('http://127.0.0.1:5000/api/send-assignment-notification', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(notificationData),
      });

      const result = await response.json();
      if (response.ok) {
          console.log(result.msg);
          alert("Volunteer successfully matched and notification sent.");
      } else {
          alert(result.msg);
      }
  } catch (error) {
      console.error("Failed to send notification:", error);
      alert("An error occurred while sending the notification.");
  }
};


  return (
    <div className="page-container">
      {/* Header banner */}
      <Navbar />
      <header style={styles.header}>People & Event Matcher</header>

      <main className="main-content">
        {/* Alert message display */}
        {alertMessage && <div style={styles.alert}>{alertMessage}</div>}

        {/* Events list container */}
        <ul style={styles.eventList}>
          {events.map((event, index) => (
            <li key={index} style={styles.eventItem}>
              <h2>{event.name}</h2>
              <p><strong>Date:</strong> {event.date}</p>
              <p><strong>Location:</strong> {event.location}</p>
              <p><strong>Description:</strong> {event.description}</p>
              <p><strong>Skills:</strong> {event.skills || "No Required Skills"}</p>

              {/* Dropdown for user selection */}
              <select
                onChange={(e) => 
                  {const selectedUserEmail = e.target.value;
                  setSelectedEvents(prev => ({ ...prev, [event.name]: selectedUserEmail }));}}
              style={styles.dropdown}
              >
                <option value="">Select a user</option>
                {people.map((user) => (
                  <option
                    key={user.id}
                    value={user.email} // Display the user's name in the dropdown
                    title={`Availability: ${user.availability || "Not Avaliable"}, Skills: ${user.skills || ""}`} // Tooltip with user's availability
                  >
                    {user.fullname} ({user.email}) {/* Optionally show email */}
                  </option>
                ))}
              </select>

              {/* Confirm button */}
              <button
                onClick={() => handleConfirm(event.name)}
                style={styles.button}
              >
                Confirm Match
              </button>
            </li>
          ))}
        </ul>
      </main>
      <Footer />
    </div>
  );
};

// Basic inline styles for the component
const styles = {
  header: {
    backgroundColor: '#28a745',
    color: 'white',
    textAlign: 'center',
    padding: '20px 0',
    marginBottom: '20px',
    fontSize: '2em'
  },
  eventList: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
    padding: '0 20px',
    listStyle: 'none',
    margin: 0
  },
  eventItem: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    transition: 'transform 0.2s',
    textAlign: 'left'
  },
  dropdown: {
    marginTop: '10px',
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc'
  },
  button: {
    marginTop: '10px',
    padding: '10px',
    borderRadius: '5px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    cursor: 'pointer'
  }
};

export default PeopleEventMatcher;
