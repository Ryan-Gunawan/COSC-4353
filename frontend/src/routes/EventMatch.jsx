import React, { useState, useEffect } from 'react';
import Navbar from "../components/Navbar/Navbar";
import Footer from '../components/Footer/Footer';

const PeopleEventMatcher = () => {
  const [people, setPeople] = useState([]);
  const [events, setEvents] = useState([]);
  const [selectedEvents, setSelectedEvents] = useState({}); // For selected events per user
  const [loading, setLoading] = useState(true); // Loading state for users

  // Fetch users from the new API route
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/usersList');
        const usersData = await response.json();
        console.log("Fetched users data:", usersData);
  
        // Check if the data is wrapped in a 'users' key, extract the array if needed
        if (usersData.users) {
          setPeople(usersData.users);  // Set the 'users' array from the fetched data
        } else {
          console.log("Broken")
          setPeople([]);  // Fallback if data format is unexpected
        }
  
        setLoading(false); // Set loading to false after fetching
      } catch (error) {
        console.error('Error fetching users:', error);
        setLoading(false); // Stop loading even on error
      }
    };
  
    fetchUsers();
  }, []); // Run only once on component mount

  // Fetch events (if not hardcoded) - you can implement a similar fetch for events
  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const eventsResponse = await fetch('http://127.0.0.1:5000/api/eventlist');
        const eventsData = await eventsResponse.json();
        setEvents(eventsData); // Update state with fetched events
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    };

    fetchEvents();
  }, []);

  // Handle event selection
  const handleEventChange = (personName, eventName) => {
    setSelectedEvents(prev => ({
      ...prev,
      [personName]: eventName
    }));
  };

  // Function to check if the person has the required skills for the selected event
  const hasRequiredSkills = (personSkills, eventSkills) => {
    return eventSkills.every(skill => personSkills.includes(skill));
  };

  // Handle confirm button click
  const handleConfirm = (personName) => {
    const selectedEventName = selectedEvents[personName];
    const selectedEvent = events.find(event => event.name === selectedEventName);
    const person = people.find(p => p.fullname === personName);

    if (selectedEvent && person) {
      const isMatch = hasRequiredSkills(person.skills, selectedEvent.skills);

      if (isMatch) {
        alert(`${personName} is successfully matched with ${selectedEvent.name}!`);
      } else {
        alert(`${personName} does not have the required skills for ${selectedEvent.name}.`);
      }
    }
  };

  // If still loading users, display a loading message
  if (loading) {
    return <div>Loading users...</div>;
  }

  return (
    <div className="page-container">
      <Navbar />
      <header style={styles.header}>People & Event Matcher</header>

      <main className="main-content">
        <ul style={styles.eventList}>
          {events.map((event, index) => (
            <li key={index} style={styles.eventItem}>
              {/* Display event details */}
              <h2>{event.name}</h2>
              <p><strong>Date:</strong> {event.date}</p>
              <p><strong>Location:</strong> {event.location}</p>
              <p><strong>Description:</strong> {event.description}</p>

              {/* Dropdown for user selection */}
              <select
                onChange={(e) => handleUserChange(event.name, e.target.value)}
                style={styles.dropdown}
              >
                <option value="">Select a user</option>
                {people.map((person, idx) => (
                  <option
                    key={idx}
                    value={person.fullname || person.email}
                    title={`Skills: ${Array.isArray(person.skills) ? person.skills.join(', ') : 'No skills listed'} Availability: ${Array.isArray(person.availability) ? person.availability.join(', ') : 'No availability listed'}`} // Tooltip with skills
                  >
                    {person.fullname || person.email}
                  </option>
                ))}
              </select>

              {/* Confirm button */}
              <button
                onClick={() => handleConfirm(event.name)}
                style={styles.button}
                disabled={!selectedEvents[event.name]} // Disable if no user selected
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
  peopleList: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
    padding: '0 20px',
    listStyle: 'none',
    margin: 0
  },
  personItem: {
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

