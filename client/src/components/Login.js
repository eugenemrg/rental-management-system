import React from 'react';
import '../App.css';
import email_icon from '../Images/email_icon.png';
import password_icon from '../Images/password_icon.png';

function Login() {
  return (
    <div className='login'>
      <div className='header'>
        <div className="text">Login</div>
        <div className="underline"></div> 
      </div>
      <div className="inputs">
        <div className="input">
          <img src={email_icon} alt="" className='icon'/>
          <input type="email" placeholder='Email address'/>
        </div>
        <div className="input">
          <img src={password_icon} alt="" className='icon'/>
          <input type="password" placeholder='Password'/>
        </div>
        <div className='forgot-password'>Lost Password?<span> Click Here!</span></div>
        
        <div className='submit-container'> 
          <div className='submit'>Log in</div>
        </div>
      </div>
    </div>
  );
}

export default Login;
