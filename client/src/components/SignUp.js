import React from 'react';
import '../App.css';
import user_icon from '../Images/user_icon.png';
import email_icon from '../Images/email_icon.png';
import password_icon from '../Images/password_icon.png';

function SignUp() {
  return (
    <div className='login'>
      <div className='header'>
        <div className="text">Sign Up</div>
        <div className="underline"></div> 
      </div>
      <div className="inputs">
        <div className="input">
          <img src={user_icon} alt="" className='icon'/>
          <input type="text" placeholder='Name'/>
        </div>
        <div className="input">
          <img src={email_icon} alt="" className='icon'/>
          <input type="email" placeholder='Email address'/>
        </div>
        <div className="input">
          <img src={password_icon} alt="" className='icon'/>
          <input type="password" placeholder='Password'/>
        </div>
        <div className="input">
          <img src={password_icon} alt="" className='icon'/>
          <input type="password" placeholder='Confirm password'/>
        </div>
        
        <div className='submit-container'> 
          <div className='submit'>Sign Up</div>
        </div>
      </div>
    </div>
  );
}

export default SignUp;
