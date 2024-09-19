import Navbar from "../../components/Navbar/Navbar"
import './HomePage.css'
import heroimage from '../../components/Assets/heroimage.jpg'

function HomePage() {

  return (
    <>
      <header>
        <Navbar />
      </header>

      <body>
        <div className="hero-container">
          <h1 className="hero-title">Connect with Volunteer Opportunities</h1>
          <button className="hero-button">Find Opportunities</button>
        </div>
      </body>
    </>
  )
}
export default HomePage
