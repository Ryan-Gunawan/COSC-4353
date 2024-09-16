import React from 'react';
import Navbar from "../components/Navbar/Navbar"

const PeopleList = () => {
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

  return (
    <div>
      {/* Header banner */}
      <Navbar />
      <header style={styles.header}>People Directory</header>

      {/* People list container */}
      <ul style={styles.peopleList}>
        {people.map((person, index) => (
          <li key={index} style={styles.personItem}>
            <h2>{person.name}</h2>
            <p><strong>Location:</strong> {person.location}</p>
            <p><strong>Skills:</strong> {person.skills.join(', ')}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

// Basic inline styles for the component (optional, you can move them to a CSS file)
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
  }
};

export default PeopleList;
