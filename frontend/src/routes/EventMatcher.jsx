import React from 'react';
import Navbar from "../components/Navbar/Navbar"

const EventList = () => {
  // Hardcoded event details
  const events = [
    {
      name: "Tech Conference 2024",
      date: "2024-10-15",
      location: "San Francisco, CA",
      description: "Join us for a day of insightful talks and networking with industry leaders in technology."
    },
    {
      name: "Music Festival",
      date: "2024-09-25",
      location: "Austin, TX",
      description: "A weekend filled with live music performances from top artists around the world."
    },
    {
      name: "Startup Pitch Night",
      date: "2024-11-05",
      location: "New York, NY",
      description: "Watch innovative startups pitch their ideas to investors and compete for prizes."
    }
  ];

  return (
    <div>
      {/* Header banner */}
      <header style={styles.header}>Upcoming Events</header>
      <Navbar />

      {/* Event list container */}
      <ul style={styles.eventList}>
        {events.map((event, index) => (
          <li key={index} style={styles.eventItem}>
            <h2>{event.name}</h2>
            <p><strong>Date:</strong> {event.date}</p>
            <p><strong>Location:</strong> {event.location}</p>
            <p>{event.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

const styles = {
  header: {
    backgroundColor: '#007bff',
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
  }
};

export default EventList;
