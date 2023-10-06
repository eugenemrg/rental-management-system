import React, { useEffect, useState } from 'react'
import {Link} from 'react-router-dom'
import './Base.css'
import { useSignOut } from 'react-auth-kit'

function Nav() {
  const signOut = useSignOut()
  const [clicks, setClicks] = useState(0)

  useEffect(() => {
    if(clicks > 0){
      signOut()
    }
  }, [clicks])

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
            <span className='logout-button' onClick={e => setClicks(c => c+1)}>Log Out</span>
        </div>
    </div>
  )
}

export default Nav