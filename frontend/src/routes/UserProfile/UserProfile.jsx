import "./userprofile.css";

function UserProfile(){

    return(
        <>
        
        <div className="userprofilepage">
            <br/><label className="instruction">Complete your profile before proceeding to home page</label><br/><br/>
            <div className="centered-square">
                <form>
                    <div className="pad-10">
                        <label>Full name</label>
                        <label className="required">*</label><br/>
                        <input className="inputbox" type="text" name="fullname" maxLength="50" required></input>
                    </div>
                    <div className="pad-10">
                        <label>Address 1</label>
                        <label className="required">*</label><br/>
                        <input className="inputbox" type="text" name="address1" maxLength="100" required></input>
                    </div>
                    <div className="pad-10">
                        <label>Address 2 </label><br/>
                        <input className="inputbox" type="text" name="address1" maxLength="100"></input>
                    </div>
                    <div className="pad-10">
                        <label>City</label>
                        <label className="required">*</label><br/>
                        <input className="inputbox" type="text" name="city" maxLength="100" required></input>
                    </div>
                    <div className="pad-10">
                        <label>State</label>
                        <label className="required">*</label><br/>
                        <select className= "state-box" name="state" required>
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
                        <label className="required">*</label><br/>
                        <input className="inputbox" type="text" name="zipcode" maxLength="9" minLength="5" required></input>
                    </div>
                    <div className="pad-10">
                        <label>Skills</label>
                        <label className="required">*</label><br/>
                        <select className="selectbox" name="skills" size="2" multiple required>
                            <option value="adaptability">Adaptability</option>
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
                    </div>
                    <div className="pad-10">
                        <label>Preference</label><br/>
                        <textarea className="inputbox" name="preferences"></textarea>
                    </div>
                    <div className="pad-10">
                        <label>Availability</label>
                        <label className="required">*</label><br/>
                        <input className="inputbox" type="date" multiple required></input>
                    </div>
                    <div className="pad-10">
                        <button type="Submit">Submit</button>
                    </div>
                </form>
            </div>
            </div>
        <br/>
    </>
    )
}

export default UserProfile