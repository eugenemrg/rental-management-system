import React, { useState } from 'react';
import '../App.css';
import email_icon from '../Images/email_icon.png';
import password_icon from '../Images/password_icon.png';
import { useSignIn } from 'react-auth-kit'

function Login() {
  const signIn = useSignIn()
  let [email, setEmail] = useState('')
  let [password, setPassword] = useState('')

  let userInfo = {
    email: email,
    password: password
  }

  function handleSubmit(e) {
    e.preventDefault()
    e.stopPropagation()

    fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userInfo)
    })
      .then(res => {
        //handle status code check
        return res.json()
      })
      .then(data => {
        if (data.access_token) {
          console.log(data.access_token)
          signIn({
            token: data.access_token,
            expiresIn: 3600,
            tokenType: "Bearer",
            authState: { email: email }
          })
        } else {
          // handle redirect or error message
        }
      })

  }

  return (
    <form onSubmit={handleSubmit}>
      <div className='login'>
        <div className='header'>
          <div className="text">Login</div>
          <div className="underline"></div>
        </div>
        <div className="inputs">
          <div className="input">
            <img src={email_icon} alt="" className='icon' />
            <input type="email" placeholder='Email address' value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="input">
            <img src={password_icon} alt="" className='icon' />
            <input type="password" placeholder='Password' value={password} onChange={e => setPassword(e.target.value)} />
          </div>
          <div className='forgot-password'>Lost Password?<span> Click Here!</span></div>

          <div className='submit-container'>
            <input type='submit' className='submit' value='Log in' />
          </div>
        </div>
      </div>
    </form>
  );
}

export default Login;
