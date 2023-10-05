import React from 'react'
import {Link} from 'react-router-dom'
import Navigation from './Navigation'
import properties from '../properties.svg'
import house from '../house.svg'
import tenants from '../tenants.svg'
import issues from '../issues.svg'

function Home() {
    return (
        <>
            <Navigation />
            <div className='sections-container'>
                <p className='section-title'>dashboard</p>
                <p className='header'>RENTAL | TRACKER</p>
                <div className='section-links'>
                    <Link className='section-link-card' to='/properties'>
                        <div><img src={properties}></img></div>
                        <p>Properties</p>
                        <p>View and manage all your properties</p>
                    </Link>
                    <Link className='section-link-card' to='/houses'>
                        <div><img src={house}></img></div>
                        <p>Houses</p>
                        <p>Manage all houses linked to properties you own</p>
                    </Link>
                    <Link className='section-link-card' to='/tenants'>
                        <div><img src={tenants}></img></div>
                        <p>Tenants</p>
                        <p>View and manage all your tenants</p>
                    </Link>
                    <Link className='section-link-card' to='/issues'>
                        <div><img src={issues}></img></div>
                        <p>Issues</p>
                        <p>Track and resolve existing issues</p>
                    </Link>
                </div>
            </div>
        </>
    )
}

export default Home