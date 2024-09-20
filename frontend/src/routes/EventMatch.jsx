import React, { useState } from 'react';
import Navbar from "../components/Navbar/Navbar"
import Footer from '../components/Footer/Footer';

const PeopleEventMatcher = () => {
 // Hardcoded people details
 const people = [
  {
    name: "John Doe",
    location: "New York, NY",
    skills: ["JavaScript", "React", "Node.js", "Patience"]
  },
  {
    name: "Jane Smith",
    location: "San Francisco, CA",
    skills: ["Python", "Data Science", "Machine Learning", "Communication"]
  },
  {
    name: "Alice Johnson",
    location: "Austin, TX",
    skills: ["UI/UX Design", "Figma", "Adobe XD", "Communication", "Patience"]
  }
];

// Hardcoded event details
const events = [
  {
    eventName: "Tech Conference 2024",
    description: "Join us for a day of insightful talks and networking with industry leaders in technology.",
    location: "San Francisco, CA",
    skills: ["JavaScript", "React"],
    urgency: "High",
    eventDate: "2024-10-15"
  },
  {
    eventName: "Music Festival",
    description: "A weekend filled with live music performances from top artists around the world.",
    location: "Austin, TX",
    skills: ["Patience", "Communication"],
    urgency: "Low",
    eventDate: "2024-09-25"
  },
  {
    eventName: "Startup Pitch Night",
    description: "Watch innovative startups pitch their ideas to investors and compete for prizes.",
    location: "New York, NY",
    skills: ["Presentation", "Communication"],
    urgency: "Medium",
    eventDate: "2024-11-05"
  }
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

    // Function to check if the person has the required skills for the selected event
    const hasRequiredSkills = (personSkills, eventSkills) => {
      return eventSkills.every(skill => personSkills.includes(skill));
    };

  // Handle confirm button click
  const handleConfirm = (personName) => {
    const selectedEventName = selectedEvents[personName];
    const selectedEvent = events.find(event => event.eventName === selectedEventName);
    const person = people.find(p => p.name === personName);

    if (selectedEvent && person) {
      const isMatch = hasRequiredSkills(person.skills, selectedEvent.skills);
      
      if (isMatch) {
        alert(`${personName} is successfully matched with ${selectedEvent.eventName}!`);
      } else {
        alert(`${personName} does not have the required skills for ${selectedEvent.eventName}.`);
      }
    }
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
                <option 
                  key={idx} 
                  value={event.eventName}
                  title={`Skills required: ${event.skills.join(', ')}`}  // Tooltip with required skills
                >
                  {event.eventName}
                </option>
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