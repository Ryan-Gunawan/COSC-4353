import Navbar from "../../components/Navbar/Navbar"
import './HomePage.css'
import Footer from "../../components/Footer/Footer"

function HomePage() {

  return (
    <>
      <header>
        <Navbar />
      </header>

      <main className="home-main">
        <div className="hero">
          <div className="hero-container">
            <h1>Connect with Volunteer Opportunities</h1>
            <div className="hero-button-container">
              <a href="/eventlist"><button className="hero-button">Find Opportunities</button></a>
            </div>
          </div>
        </div>

        <div className="home-banner">
          VolunteerMatcher Near You
        </div>

        <section className="how-it-works">
          <h2>How It Works</h2>
          <div className="steps-container">
            <div className="step">
              <h3>Step 1: <a href="/">Sign Up</a></h3>
              <p>Create an account and get started as a volunteer.</p>
            </div>
            <div className="step">
              <h3>Step 2: Set up your <a href="/userprofile">Profile</a></h3>
              <p>Tell us more about your skills and interests to get personalized matches.</p>
            </div>
            <div className="step">
              <h3>Step 3: Get Matched to an <a href="/eventlist">Event</a></h3>
              <p>We will match you to events that suit your skills and preferences.</p>
            </div>
          </div>
        </section>

        <section className="benefits">
          <h2>Benefits of Volunteering</h2>
          <div className="benefits-container">
            <div className="benefit">
              <h3>Make a Difference</h3>
              <p>Contribute to meaningful causes and help your community thrive.</p>
            </div>
            <div className="benefit">
              <h3>Gain New Skills</h3>
              <p>Learn valuable skills that can enhance your career and personal growth.</p>
            </div>
            <div className="benefit">
              <h3>Meet New People</h3>
              <p>Connect with like-minded individuals and expand your social network.</p>
            </div>
          </div>
        </section>

      </main>
      <Footer />

    </>
  )
}
export default HomePage
