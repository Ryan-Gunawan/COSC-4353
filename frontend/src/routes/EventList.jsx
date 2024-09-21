import React, {useState} from 'react';
import Navbar from "../components/Navbar/Navbar"
import Footer from '../components/Footer/Footer';


const EventList = () => {
  // Hardcoded event details as state to allow modifications
  const [events, setEvents] = useState([
    {
      id: 1,
      name: "Tech Conference 2024",
      date: "2024-10-15",
      location: "San Francisco, CA",
      description: "Join us for a day of insightful talks and networking with industry leaders in technology.",
      isDeleting: false
    },
    {
      id: 2,
      name: "Music Festival",
      date: "2024-09-25",
      location: "Austin, TX",
      description: "A weekend filled with live music performances from top artists around the world.",
      isDeleting: false
    },
    {
      id: 3,
      name: "Startup Pitch Night",
      date: "2024-11-05",
      location: "New York, NY",
      description: "Watch innovative startups pitch their ideas to investors and compete for prizes.",
      isDeleting: false
    }
  ]);

    // For editing event
    const [editingEvent, setEditingEvent] = useState(null);
    const [formData, setFormData] = useState({
      name: "",
      date: "",
      location: "",
      description: ""
    });
  
    // Handle input changes for the edit form
    const handleInputChange = (e) => {
      setFormData({
        ...formData,
        [e.target.name]: e.target.value
      });
    };
  
  // Delete event - set the background red first
  const deleteEvent = (id) => {
    setEvents(events.map(event => 
      event.id === id ? { ...event, isDeleting: true } : event
    ));

    // Delay removal to allow the red background effect
    setTimeout(() => {
      setEvents(events.filter(event => event.id !== id));
    }, 1000); // 1 second delay before actual deletion
  };
  
    // Edit event - populate the form with event data
    const editEvent = (event) => {
      setEditingEvent(event.id);
      setFormData({
        name: event.name,
        date: event.date,
        location: event.location,
        description: event.description
      });
    };
  
    // Save the edited event
    const saveEvent = () => {
      setEvents(events.map(event =>
        event.id === editingEvent
          ? { ...event, ...formData }
          : event
      ));
      setEditingEvent(null);
    };

  return (
    <div className="page-container">
      {/* Header banner */}
      <Navbar />
      <header style={styles.header}>Upcoming Events</header>

      <main className="main-content">
        {/* Event list container */}
        <ul style={styles.eventList}>
        {events.map(event => (
          <li key={event.id} style={styles.eventItem}>
            {editingEvent === event.id ? (
              <div>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Event Name"
                />
                <input
                  type="date"
                  name="date"
                  value={formData.date}
                  onChange={handleInputChange}
                />
                <input
                  type="text"
                  name="location"
                  value={formData.location}
                  onChange={handleInputChange}
                  placeholder="Location"
                />
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  placeholder="Description"
                />
                <button onClick={saveEvent}>Save</button>
              </div>
            ) : (
              <div>
                <h2>{event.name}</h2>
                <p><strong>Date:</strong> {event.date}</p>
                <p><strong>Location:</strong> {event.location}</p>
                <p>{event.description}</p>
                <button onClick={() => editEvent(event)}>Edit</button>
                <button onClick={() => deleteEvent(event.id)}>Delete</button>
              </div>
            )}
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
    backgroundColor: '#009692',
    color: 'white',
    textAlign: 'center',
    padding: '20px 0',
    marginLeft: '300px',
    marginRight: '300px',
    marginBottom: '20px',
    fontSize: '2em',
    borderRadius: '10px',
  },
  eventList: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
    padding: '0 300px',
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
