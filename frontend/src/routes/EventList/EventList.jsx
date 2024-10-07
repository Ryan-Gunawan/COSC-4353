import {useState, useEffect} from 'react';
import Navbar from "../../components/Navbar/Navbar"
import Footer from '../../components/Footer/Footer';
import './EventList.css'


const EventList = () => {
  // Hardcoded event details as state to allow modifications
  const [events, setEvents] = useState([]);
  const [editingEvent, setEditingEvent] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    date: "",
    location: "",
    description: ""
  });

  // Fetch events from the backend
  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/eventlist');
        const data = await response.json();
        setEvents(data);  // Set the fetched events into state
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    };
    fetchEvents();
  }, []);
  
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
        description: event.description,
        urgency: event.urgency,
        skills: event.skills
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
        <div className="create-event-button-container">
          <a href="/newevent"><button className="create-event-button">Create Event</button></a>
        </div>
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
                <input
                  type="text"
                  name="urgency"
                  value={formData.urgency}
                  onChange={handleInputChange}
                  placeholder="Urgency"
                />
                <input
                  type="text"
                  name="skills"
                  value={formData.skills.join(', ')}
                  onChange={handleInputChange}
                  placeholder="Skills (comma separated)"
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
                <p><strong>Urgency:</strong> {event.urgency ? event.urgency : 'N/A'}</p>
                <p><strong>Skills preferred:</strong> {Array.isArray(event.skills) ? event.skills.join(', ') : 'N/A'}</p>
                <p>{event.description}</p>
                <button onClick={() => editEvent(event)} style={styles.editButton}>Edit</button>
                <button onClick={() => deleteEvent(event.id)} style={styles.deleteButton}>Delete</button>
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
  },
  eventItem: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    transition: 'transform 0.2s',
    textAlign: 'left'
  },
    editButton: {
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '20px',
    cursor: 'pointer',
    marginRight: '10px',
    fontSize: '1em'
  },
  deleteButton: {
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '20px',
    cursor: 'pointer',
    fontSize: '1em'
  }
};

export default EventList;
