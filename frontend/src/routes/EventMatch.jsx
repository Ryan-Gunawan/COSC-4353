import React, { useState, useEffect } from 'react';
import Navbar from "../components/Navbar/Navbar";
import Footer from '../components/Footer/Footer';

const PeopleEventMatcher = () => {
  const [people, setPeople] = useState([]);
  const [events, setEvents] = useState([]);
  const [selectedEvents, setSelectedEvents] = useState({}); // Track selected events for each user

  // Fetch users from the API route
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/userinfo');
        const usersData = await response.json();
        const formattedUsers = Object.values(usersData).flat();
        setPeople(formattedUsers);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };
    fetchUsers();
  }, []);

  // Fetch events from the API route
  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/eventlist');
        const eventsData = await response.json();
        setEvents(eventsData);
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    };
    fetchEvents();
  }, []);

  // Handle event selection
  const handleEventChange = (personFullname, eventName) => {
    setSelectedEvents(prev => ({
      ...prev,
      [personFullname]: eventName
    }));
  };

  // Function to check if the user is available on the event date
  const isAvailableForEvent = (availabilityArray, eventDate) => {
    return availabilityArray.includes(eventDate);
  };

  const matchingSkills = (skillArray, eventSkills) => {
    return skillArray.includes(eventSkills);
  };

  // Handle confirm button click
  const handleConfirm = (personFullname) => {
    const selectedEventName = selectedEvents[personFullname];
    const selectedEvent = events.find(event => event.name === selectedEventName);
    const person = people.find(p => p.fullname === personFullname);

    if (selectedEvent && person) {
      // Check if the user is available for the event date
      const isAvailable = isAvailableForEvent(person.availability, selectedEvent.date);
      const hasSkills = matchingSkills(person.skills, selectedEvent.skills)

      if (hasSkills && isAvailable) {
        alert(`${personFullname} is successfully matched with ${selectedEvent.name}!`);
      } else if (!hasSkills) {
        alert(`${personFullname} does not have the required skills for ${selectedEvent.name}.`);
      } else if (!isAvailable) {
        alert(`${personFullname} is not available on the date of ${selectedEvent.name}.`);
      }
    }
  };

  return (
    <div className="page-container">
      {/* Header banner */}
      <Navbar />
      <header style={styles.header}>People & Event Matcher</header>

      <main className="main-content">
        {/* People list container */}
        <ul style={styles.peopleList}>
          {people.map((person, index) => (
            <li key={index} style={styles.personItem}>
              <h2>{person.fullname}</h2>
              <p><strong>Address:</strong> {`${person.address1}, ${person.address2 ? person.address2 + ', ' : ''}${person.city}, ${person.state} ${person.zipcode}`}</p>
              <p><strong>Skills:</strong> {person.skills.join(', ')}</p>
              <p><strong>Availability:</strong> {person.availability.length > 0 ? person.availability.join(', ') : "No availability"}</p>
              <p><strong>Preference:</strong> {person.preference}</p>

              {/* Dropdown for event selection */}
              <select
                onChange={(e) => handleEventChange(person.fullname, e.target.value)}
                style={styles.dropdown}
              >
                <option value="">Select an event</option>
                {events.map((event, idx) => (
                  <option
                    key={idx}
                    value={event.name}
                    title={`Event Date: ${event.date}, Event Skills: ${event.skills}`} // Tooltip with event date
                  >
                    {event.name} - {event.location}
                  </option>
                ))}
              </select>

              {/* Confirm button */}
              <button
                onClick={() => handleConfirm(person.fullname)}
                style={styles.button}
                disabled={!selectedEvents[person.fullname]} // Disable if no event selected
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
