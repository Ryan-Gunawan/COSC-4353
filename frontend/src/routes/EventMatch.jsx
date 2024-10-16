import React, { useState, useEffect } from 'react';
import Navbar from "../components/Navbar/Navbar";
import Footer from '../components/Footer/Footer';

const PeopleEventMatcher = () => {
  const [people, setPeople] = useState([]);
  const [events, setEvents] = useState([]);

  // Fetch users and events from the API on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch users from the Flask API
        const usersResponse = await fetch('http://127.0.0.1:5000/api/users');
        const usersData = await usersResponse.json();
        
        // Map users data to match the required fields
        const mappedUsers = usersData.map(user => ({
          name: user.email,          // Assuming email is used for display
          location: "Unknown",       // Adjust if needed
          skills: ["Unknown"],       // Replace with actual skills if available
        }));
        setPeople(mappedUsers); // Set the mapped users to state

        // Fetch events from the Flask API
        const eventsResponse = await fetch('http://127.0.0.1:5000/api/eventlist');
        const eventsData = await eventsResponse.json();
        
        // Map events data to match the required fields (assuming you're manually adding skills and urgency)
        const mappedEvents = eventsData.map(event => ({
          eventID: event.id,
          eventName: event.name,           // Using event name
          eventDate: event.date,         // Event date
          location: event.location,       // Event location
          description: event.description, // Event description
          eventSkills: event.skills, // Example skills (replace with actual skills)
        }));
        setEvents(mappedEvents); // Set the mapped events to state
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []); // Empty dependency array means this will only run once when the component mounts

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
    <div className="page-container">
      <Navbar />
      <header style={styles.header}>People & Event Matcher</header>
  
      <main className="main-content">
        <ul style={styles.peopleList}>
          {people.map((person, index) => (
            <li key={index} style={styles.personItem}>
              <h2>{person.name}</h2>
              <p><strong>Location:</strong> {person.location || "Not provided"}</p>
              <p><strong>Skills:</strong> {person.skills?.length > 0 ? person.skills.join(', ') : "Skills not listed"}</p>
  
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
                    title={`Skills required: ${event.skills?.join(', ') || "None specified"}`} // Tooltip with required skills
                  >
                    {event.eventName} - {event.urgency || "Urgency not listed"}
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
      </main>
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
