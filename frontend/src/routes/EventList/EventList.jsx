import { useState, useEffect } from 'react';
import Navbar from "../../components/Navbar/Navbar";
import Footer from '../../components/Footer/Footer';
import './EventList.css';

const EventList = () => {
  const [events, setEvents] = useState([]);
  const [editingEvent, setEditingEvent] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    date: "",
    location: "",
    description: "",
    urgency: "",
    skills: [],
  });

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/eventlist');
        const data = await response.json();
        setEvents(data);
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    };
    fetchEvents();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: name === 'skills' ? value.split(',').map(skill => skill.trim()) : value,
    }));
  };

  const deleteEvent = (id) => {
    setEvents((prevEvents) => prevEvents.map(event => 
      event.id === id ? { ...event, isDeleting: true } : event
    ));

    setTimeout(() => {
      setEvents((prevEvents) => prevEvents.filter(event => event.id !== id));
    }, 1000);
  };

  const editEvent = (event) => {
    setEditingEvent(event.id);
    setFormData({
      name: event.name,
      date: event.date,
      location: event.location,
      description: event.description,
      urgency: event.urgency || '',
      skills: event.skills || [],
    });
  };

  const saveEvent = async () => {
    try {
      await fetch(`http://127.0.0.1:5000/api/eventlist/${editingEvent}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      setEvents((prevEvents) =>
        prevEvents.map(event =>
          event.id === editingEvent ? { ...event, ...formData } : event
        )
      );
      setEditingEvent(null);
    } catch (error) {
      console.error("Error saving event:", error);
    }
  };

  return (
    <div className="page-container">
      <Navbar />
      <header style={styles.header}>Upcoming Events</header>
      <main className="main-content">
        <div className="create-event-button-container">
          <a href="/newevent"><button className="create-event-button">Create Event</button></a>
        </div>
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
                    value={formData.skills.join(', ')} // This assumes skills is an array
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
