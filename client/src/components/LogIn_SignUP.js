import React, { useState } from 'react';
import '../App.css';
import user_icon from '../Images/user_icon.png';
import email_icon from '../Images/email_icon.png';
import password_icon from '../Images/password_icon.png';
import add_user_icon from '../Images/add_user_icon.png';

function LogIn_SignUp() {
  
  const [action, setAction] = useState("Sign Up");

  return (
    <div className='login'>
      <div className='header'>
        <div className="text">{action}</div>
        <div className="underline"></div> 
      </div>
      <div className="inputs">
        {action==="Login"?<div></div>:<div className="input">
          <img src={user_icon} alt="" className='icon'/>
          <input type="text" placeholder='Name'/>
        </div>}

        
        <div className="input">
          <img src={email_icon} alt="" className='icon'/>
          <input type="email" placeholder='Email address'/>
        </div>
        <div className="input">
          <img src={password_icon} alt="" className='icon'/>
          <input type="password" placeholder='Password'/>
        </div>
        {action==="SignUp"?<div></div>:<div className='forgot-password'>Lost Password?<span> Click Here!</span></div>}
        
        <div className='submit-container'> 
          <div className={action === "Login" ? 'submit gray' : "submit"}onClick={()=>{setAction("Sign Up")}}>Sign Up</div>
          <div className={action === "Sign Up" ? 'submit gray' : "submit"}onClick={()=>{setAction("Login")}}>Log in</div>
        </div>
      </div>
    </div>
  );
}

export default LogIn_SignUp;
