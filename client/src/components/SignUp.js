import React, { useState } from 'react';
import '../App.css';
import user_icon from '../Images/user_icon.png';
import email_icon from '../Images/email_icon.png';
import password_icon from '../Images/password_icon.png';

function SignUp() {
  let [name, setName] = useState('')
  let [email, setEmail] = useState('')
  let [password, setPassword] = useState('')
  let [confirmPassword, setConfirmPassword] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    e.stopPropagation()

    // Handle requests
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className='login'>
        <div className='header'>
          <div className="text">Sign Up</div>
          <div className="underline"></div>
        </div>
        <div className="inputs">
          <div className="input">
            <img src={user_icon} alt="" className='icon' />
            <input type="text" placeholder='Name' value={name} onChange={e => setName(e.target.value)} />
          </div>
          <div className="input">
            <img src={email_icon} alt="" className='icon' />
            <input type="email" placeholder='Email address' value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="input">
            <img src={password_icon} alt="" className='icon' />
            <input type="password" placeholder='Password' value={password} onChange={e => setPassword(e.target.value)} />
          </div>
          <div className="input">
            <img src={password_icon} alt="" className='icon' />
            <input type="password" placeholder='Confirm password' value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
          </div>

          <div className='submit-container'>
          <input type='submit' className='submit' value='Sign Up'/>
          </div>
        </div>
      </div>
    </form>
  );
}

export default SignUp;
