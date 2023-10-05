import React from 'react'
import {Link} from 'react-router-dom'
import './Base.css'

function Nav() {
  return (
    <div className='navigation'>
        <div className='links'>
            <Link to='/dashboard' className='home-link'>rtm</Link>
            <Link to='/properties'>Properties</Link>
            <Link to='/houses'>Houses</Link>
            <Link to='/issues'>Reports/Issues</Link>
            <Link to='/tenants'>Tenants</Link>
        </div>
        <div className='buttons'>
            <span className='logout-button'>Log Out</span>
        </div>
    </div>
  )
}

export default Nav