import React, { useState } from 'react';
import Navbar from "../components/Navbar/Navbar"

const PeopleEventMatcher = () => {
  // Hardcoded people details
  const people = [
    {
      name: "John Doe",
      location: "New York, NY",
      skills: ["JavaScript", "React", "Node.js"]
    },
    {
      name: "Jane Smith",
      location: "San Francisco, CA",
      skills: ["Python", "Data Science", "Machine Learning"]
    },
    {
      name: "Alice Johnson",
      location: "Austin, TX",
      skills: ["UI/UX Design", "Figma", "Adobe XD"]
    }
  ];

  // Hardcoded event names
  const events = [
    "Tech Conference 2024",
    "Music Festival",
    "Startup Pitch Night"
  ];

  // State to store selected event for each person
  const [selectedEvents, setSelectedEvents] = useState({});

  // Handle event selection
  const handleEventChange = (personName, eventName) => {
    setSelectedEvents(prev => ({
      ...prev,
      [personName]: eventName
    }));
  };

  // Handle confirm button click
  const handleConfirm = (personName) => {
    alert(`${personName} is matched with ${selectedEvents[personName]}`);
  };

  return (
    <div>
      {/* Header banner */}
      <Navbar />
      <header style={styles.header}>People & Event Matcher</header>

      {/* People list container */}
      <ul style={styles.peopleList}>
        {people.map((person, index) => (
          <li key={index} style={styles.personItem}>
            <h2>{person.name}</h2>
            <p><strong>Location:</strong> {person.location}</p>
            <p><strong>Skills:</strong> {person.skills.join(', ')}</p>

            {/* Dropdown for event selection */}
            <select 
              onChange={(e) => handleEventChange(person.name, e.target.value)}
              style={styles.dropdown}
            >
              <option value="">Select an event</option>
              {events.map((event, idx) => (
                <option key={idx} value={event}>{event}</option>
              ))}
            </select>

            {/* Confirm button */}
            <button 
              onClick={() => handleConfirm(person.name)} 
              style={styles.button}
              disabled={!selectedEvents[person.name]} // Disable if no event selected
            >
              Confirm Match
            </button>
          </li>
        ))}
      </ul>
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
