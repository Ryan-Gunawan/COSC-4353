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
    // Ensure both are arrays before calling some
    if (!Array.isArray(personSkills) || !Array.isArray(requiredSkills)) {
        return false;
    }
    
    // Normalize skills to lower case and trim whitespace
    const normalizedPersonSkills = personSkills.map(skill => skill.toLowerCase().trim());
    const normalizedRequiredSkills = requiredSkills.map(skill => skill.toLowerCase().trim());

    // Check if at least one required skill is in person's skills
    return normalizedRequiredSkills.some(skill => normalizedPersonSkills.includes(skill));
};

  // Function to check if the person is available for the event
  const isAvailable = (personAvailability, eventDate) => {
    return personAvailability.includes(eventDate);
  };

// Handle confirm button click
const handleConfirm = (eventName) => {
  // Get the selected user's email based on the event name
  const selectedUserEmail = selectedEvents[eventName]; 
  console.log("Selected User Email:", selectedUserEmail); // Debugging log

  // Check if selectedUserEmail is valid
  if (!selectedUserEmail) {
      setAlertMessage("No user selected for this event.");
      return;
  }

  // Find the selected event
  const selectedEvent = events.find(event => event.name === eventName);
  // Find the person by email
  const person = people.find(p => p.email === selectedUserEmail); 
  // Check if person exists and has a volunteer array
  if (person) {
    if (!Array.isArray(person.volunteer)) {
      person.volunteer = []; // Initialize if not an array
        }
      }
  if (selectedEvent && person) {
    const requiredSkills = Array.isArray(selectedEvent.skills) ? selectedEvent.skills : [];
    // Check if the person's skills are defined
    // Use the hasRequiredSkills function to check for skills
    const hasSkills = hasRequiredSkills(person.skills, requiredSkills);

    const available = person.availability && person.availability.length > 0 
        ? isAvailable(person.availability, selectedEvent.date) 
        : true;

    // Check if the volunteer is already matched to the event
    if (person.volunteer.includes(selectedEvent.id)) {
        setAlertMessage(`${person.fullname || person.email} has already been matched to this event.`);
        return;
    }
    else{

    // Proceed with matching if they have the required skills or undefined skills and are available
    if (hasSkills && available) {
        person.volunteer.push(selectedEvent.id); // Add event ID to volunteer array
        setAlertMessage(`${person.fullname || person.email} is successfully matched with ${selectedEvent.name}!`);
        return;
      } else {
        setAlertMessage(`${person.fullname || person.email} does not meet the requirements for ${selectedEvent.name}.`);
        return;
      }
    }
} else {
    setAlertMessage("User or event not found.");
    return;
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
                  console.log("Dropdown Selected Email:", selectedUserEmail); // Debugging log
                  setSelectedEvents(prev => ({ ...prev, [event.name]: selectedUserEmail }));}}
              style={styles.dropdown}
              >
                <option value="">Select a user</option>
                {people.map((user) => (
                  <option
                    key={user.id}
                    value={user.email} // Display the user's name in the dropdown
                    title={`Availability: ${user.availability}, Skills: ${user.skills}`} // Tooltip with user's availability
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
  },
  alert: {
    padding: '10px',
    margin: '10px 0',
    color: 'white',
    backgroundColor: '#f44336', // Red
    borderRadius: '5px',
  },
};

export default PeopleEventMatcher;
