import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import "./newevent.css";

function NewEvent() {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    location: '',
    skills: '',
    urgency: '1', // default urgency value
    date: ''
  });

  const navigate = useNavigate();

  const handleChange = (event) => {
    const { name, value, type, selectedOptions } = event.target;

    if (type === 'select-multiple') {
      const selectedValues = Array.from(selectedOptions).map(option => option.value);
      setFormData((prevData) => ({ ...prevData, [name]: selectedValues }));
    } else {
      setFormData((prevData) => ({ ...prevData, [name]: value }));
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();  // Prevent default form submission

    try {
      // For converting datetime obj to string. But it works without having to do this.
      // const dateObj = new Date(formData.date);
      // const formattedDate = `${dateObj.getFullYear()}-${dateObj.getMonth() + 1}-${dateObj.getDate()}`;

      // Convert skills to JSON string for submission without modifying the original formData
      const formDataToSubmit = {
        ...formData,
        skills: JSON.stringify(formData.skills),
        // date: formattedDate
      };

      const response = await fetch('http://127.0.0.1:5000/api/newevent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formDataToSubmit),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log(data.message);  // Show success message
      navigate('/success');
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };


  return (
    <>
      <Navbar />
      <div className="neweventpage">
        <header><h1>Host a new event!</h1></header><br />
        <main className="centered-square">
          <form onSubmit={handleSubmit}>
            <div className="pad-10">
              <label htmlFor="name">Event name:</label><br />
              <input className="inputbox" type="text" id="name" name="name" value={formData.name} onChange={handleChange} /><br />
            </div>

            <div className="pad-10">
              <label htmlFor="description">Description:</label><br />
              <textarea className="inputbox" id="description" name="description" value={formData.description} onChange={handleChange} /><br />
            </div>

            <div className="pad-10">
              <label htmlFor="location">Location:</label><br />
              <textarea className="inputbox" id="location" name="location" value={formData.location} onChange={handleChange} /><br />
            </div>

            <div className="pad-10">
              <label htmlFor="skills">Required Skills (ctrl+left click)</label><br />
              <select className="selectbox" name="skills" id="skills" multiple value={formData.skills} onChange={handleChange}>
                <option value="organized">Organized</option>
                <option value="leadership">Leadership</option>
                <option value="goodwithchildren">Good with children</option>
                <option value="communication">Communication</option>
                <option value="problemsolver">Problem Solver</option>
                <option value="timemanagement">Time management</option>
                <option value="adaptability">Adaptability</option>
                <option value="teamwork">Teamwork</option>
                <option value="creativity">Creativity</option>
              </select><br />
            </div>

            <div className="pad-10">
              <label htmlFor="urgency">Urgency level</label><br />
              <select className="inputbox" name="urgency" id="urgency" value={formData.urgency} onChange={handleChange}>
                <option value="1">!</option>
                <option value="2">!!!</option>
                <option value="3">!!!!!</option>
              </select><br />
            </div>

            <div className="pad-10">
              <label htmlFor="date">Event date:</label><br />
              <input className="inputbox" type="datetime-local" id="Test_DatetimeLocal" name="date" min="2015-01-01T00:00" max="2025-12-31T23:59" step="1" value={formData.date} onChange={handleChange} /><br /><br />
            </div>

            <input className="submit-button" type="submit" value="Submit" />
            <br />
          </form>
        </main>
      </div>
      <Footer />
    </>
  );
}

export default NewEvent;
