import React, { useState, useEffect } from 'react';
import Navbar from "../../components/Navbar/Navbar";
import Footer from "../../components/Footer/Footer";
import "./userprofile.css";

function UserProfile() {

    const [userInfo, setUserInfo] = useState({
        id: '',
        fullname: '',
        address1: '',
        address2: '',
        city: '',
        state: '',
        zipcode: '',
        skills: [],
        preference: '',
        availability: [],
        volunteer: []
    })

    // Temporary constant while user is editing
    const [formData, setFormData] = useState({
        selectedDate: ""

    })

    useEffect(() => {
        fetch("http://localhost:5000/api/userprofile", {
            method: 'GET',
            credentials: 'include',
        })
            .then(response => {
                if (!response.ok) {
                    console.error('Unable to load user information:', response.statusText);
                    return; // Exit the promise chain
                }
                return response.json();
            })
            .then(data => {
                setUserInfo(data[0]);
                setFormData({
                    selectedDate: data[0].availability[0] || ""
                })

            })
            .catch(error => console.error('Error:', error));
    }, []);

    // Handle input change for the form fields for existing users
    const handleChange = (e) => {
        const { name, value } = e.target;

        setUserInfo(prevState => ({
            ...prevState,
            [name]: value,
        }));
    };

    // const handleMultipleChange = (item) => {
    //     console.log("item:", item)
    // if (!userInfo.skills.includes(item)) {
    //     const old_skills = userInfo.skills;
    //     console.log("skills:", userInfo.skills)
    //     const updatedSkills = [old_skills, item]
    //     console.log("UpdatedSkills:", updatedSkills)
    //     setUserInfo((prevUserInfo) => ({
    //         ...prevUserInfo,
    //         skills: [...prevUserInfo.skills, item], 
    //     }));
    // }
    //     console.log("log after", userInfo.skills)
    // };

    // useEffect(() => {
    //     console.log("Skills updated:", userInfo.skills);
    // }, [userInfo.skills]);

    // Pop up selected skills
    const handleMultipleChange = (e) => {
        const selectedOptions = Array.from(e.target.selectedOptions).map(option => option.value); // Convert selected options to an array of values
        setUserInfo((prevUserInfo) => ({
            ...prevUserInfo,
            skills: selectedOptions // Update skills with the selected options
        }));
        console.log("Updated skills:", selectedOptions); // Log the selected skills
    };

    // pop up selected dates
    const handleDateChange = (e) => {
        const date = e.target.value;
        if (date && !userInfo.availability.includes(date)) {
            setUserInfo((prevData) => ({
                ...prevData,
                availability: [...prevData.availability, date],
                // selectedDate: e.target.value
            }));
        }
    };

    // Delete selected skills/availability
    const handleRemoveItem = (type, itemToRemove) => {
        setUserInfo((prevUserInfo) => ({
            ...prevUserInfo,
            [type]: prevUserInfo[type].filter(item => item !== itemToRemove),
        }));
    };

    // Handle save button
    const saveInfo = (e) => {
        e.preventDefault();
        // try {
        fetch(`http://127.0.0.1:5000/api/userprofile/${userInfo.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userInfo),
        })
            .then((response) => {
                if (response.ok) {
                    alert('User info updated successfully');
                } else {
                    alert('Failed to update user info');
                }
            })
    };
    return (
        <>
            <Navbar />

            <div className="userprofilepage">
                <br /><label className="instruction">Complete your profile before proceeding</label><br /><br />
                <div className="centered-square">
                    <form>
                        <div className="pad-10">
                            <label>Full name</label>
                            <label className="required">*</label><br />
                            <input className="inputbox" type="text" name="fullname" maxLength="50" required value={userInfo.fullname} onChange={handleChange}></input>
                        </div>
                        <div className="pad-10">
                            <label>Address 1</label>
                            <label className="required">*</label><br />
                            <input className="inputbox" type="text" name="address1" maxLength="100" required value={userInfo.address1} onChange={handleChange}></input>
                        </div>
                        <div className="pad-10">
                            <label>Address 2 </label><br />
                            <input className="inputbox" type="text" name="address1" maxLength="100" value={userInfo.address2} onChange={handleChange}></input>
                        </div>
                        <div className="pad-10">
                            <label>City</label>
                            <label className="required">*</label><br />
                            <input className="inputbox" type="text" name="city" maxLength="100" required value={userInfo.city} onChange={handleChange}></input>
                        </div>
                        <div className="pad-10">
                            <label>State</label>
                            <label className="required">*</label><br />
                            <select className="state-box" name="state" required value={userInfo.state} onChange={handleChange}>
                                <option value="AL">Alabama</option>
                                <option value="AK">Alaska</option>
                                <option value="AZ">Arizona</option>
                                <option value="AR">Arkansas</option>
                                <option value="CA">California</option>
                                <option value="CO">Colorado</option>
                                <option value="CT">Connecticut</option>
                                <option value="DE">Delaware</option>
                                <option value="FL">Florida</option>
                                <option value="GA">Georgia</option>
                                <option value="HI">Hawaii</option>
                                <option value="ID">Idaho</option>
                                <option value="IL">Illinois</option>
                                <option value="IN">Indiana</option>
                                <option value="IA">Iowa</option>
                                <option value="KS">Kansas</option>
                                <option value="KY">Kentucky</option>
                                <option value="LA">Louisiana</option>
                                <option value="ME">Maine</option>
                                <option value="MD">Maryland</option>
                                <option value="MA">Massachusetts</option>
                                <option value="MI">Michigan</option>
                                <option value="MN">Minnesota</option>
                                <option value="MS">Mississippi</option>
                                <option value="MO">Missouri</option>
                                <option value="MT">Montana</option>
                                <option value="NE">Nebraska</option>
                                <option value="NV">Nevada</option>
                                <option value="NH">New Hampshire</option>
                                <option value="NJ">New Jersey</option>
                                <option value="NM">New Mexico</option>
                                <option value="NY">New York</option>
                                <option value="NC">North Carolina</option>
                                <option value="ND">North Dakota</option>
                                <option value="OH">Ohio</option>
                                <option value="OK">Oklahoma</option>
                                <option value="OR">Oregon</option>
                                <option value="PA">Pennsylvania</option>
                                <option value="RI">Rhode Island</option>
                                <option value="SC">South Carolina</option>
                                <option value="SD">South Dakota</option>
                                <option value="TN">Tennessee</option>
                                <option value="TX">Texas</option>
                                <option value="UT">Utah</option>
                                <option value="VT">Vermont</option>
                                <option value="VA">Virginia</option>
                                <option value="WA">Washington</option>
                                <option value="WV">West Virginia</option>
                                <option value="WI">Wisconsin</option>
                                <option value="WY">Wyoming</option>
                            </select>
                        </div>
                        <div className="pad-10">
                            <label>Zip code</label>
                            <label className="required">*</label><br />
                            <input className="inputbox" type="text" name="zipcode" maxLength="9" minLength="5" require value={userInfo.zipcode} onChange={handleChange} d></input>
                        </div>
                        <div className="pad-10">
                            <label>Skills</label>
                            <label className="required">*</label><br />

                            <select className="selectbox" name="skills" size="2" required multiple value={userInfo.skills} onChange={handleMultipleChange}>
                                <option value="adaptability"> Adaptability</option>
                                <option value="children">Good with Children</option>
                                <option value="communication">Communication</option>
                                <option value="creativity">Creativity</option>
                                <option value="responsibility">Responsibility</option>
                                <option value="flexibility">Flexibility</option>
                                <option value="leadership">Leadership</option>
                                <option value="organized">Organized</option>
                                <option value="patience">Patience</option>
                                <option value="problem">Problem Solver</option>
                                <option value="teamwork">Teamwork</option>
                                <option value="time">Time Management</option>
                            </select>

                            <div className="selected-skills">
                                {Array.isArray(userInfo.skills) && userInfo.skills.map((skill, index) => (
                                    <div key={index} className="skill-item">
                                        <p>{skill}</p>
                                        <button type="button" className="remove-skill" onClick={() => handleRemoveItem('skills', skill)}>x</button>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div className="pad-10">
                            <label>Preference</label><br />
                            <textarea className="inputbox" name="preferences" value={userInfo.preference} onChange={handleChange}></textarea>
                        </div>
                        <div className="pad-10">
                            <label>Availability</label>
                            <label className="required">*</label><br />
                            <input className="inputbox" type="date" multiple required value={formData.selectedDate} onChange={handleDateChange}></input>
                            <div className="selected-availability">
                                {userInfo.availability.map((date, index) => (
                                    <div key={index} className="availability-item">
                                        {date}
                                        <button type="button" className="remove-availability" onClick={() => handleRemoveItem('availability', date)}>x</button>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div className="pad-10">
                            <button className="saveButton" onClick={saveInfo}>Save</button>
                        </div>
                    </form>
                </div>
            </div>
            <br />
            <Footer />
        </>
    )
}

export default UserProfile
