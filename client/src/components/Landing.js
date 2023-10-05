import React from 'react'
import { Link } from 'react-router-dom'; 
import '../App.css';


function Landing() {
  return (
   
  <div className="landing-App">
  <header className="landing-header">
    <h1> rtm </h1>
    <div className="landing-login-button-container">
    <Link to="/login" className="landing-login-button">Login</Link>
    <Link to="/signup" className="landing-login-button">Sign Up</Link> 
    </div>
  </header>
  <main className="landing-main">
    <section id="about" className="landing-about">
        <h2>Rental Management System</h2>
        <p>
          Rental Management System is a powerful platform designed to help property owners manage their rental properties efficiently. 
          With rtm, you can easily keep track of your properties, tenants, and rental income, all in one place.
        </p>
    </section>
  </main>

  <footer className="landing-footer">
    <div className="landing-contact-info">
      <p>Contact Us:0700000000</p>
      <p>Email: info@rtm.com</p>
    </div>
    <p>&copy; {new Date().getFullYear()} rtm .Rental Management System</p>
  </footer>
</div>
  )
}

export default Landing 