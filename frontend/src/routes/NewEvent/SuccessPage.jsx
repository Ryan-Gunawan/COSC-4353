import { Link } from 'react-router-dom';
import './SuccessPage.css'; // Optional: Add your styling

const SuccessPage = () => {
  return (
    <div style={styles.successContainer}>
      <h1 style={styles.header}>Event Created Successfully!</h1>
      <p>Your event has been added to the list.</p>
      <Link to="/eventlist">
        <button style={styles.goToEventsButton}>Go to Event List</button>
      </Link>
    </div>
  );
};

const styles = {
  successContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f7f7f7', // Optional: Add a background color
  },
  header: {
    backgroundColor: '#009692',
    color: 'white',
    textAlign: 'center',
    padding: '20px 0',
    marginBottom: '20px',
    fontSize: '2em',
    borderRadius: '10px',
  },
  goToEventsButton: {
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '20px',
    cursor: 'pointer',
    fontSize: '1em',
  },
};

export default SuccessPage;
