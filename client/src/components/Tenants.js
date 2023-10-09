import React, { useEffect, useState } from 'react'
import './Base.css'
import Table from 'react-bootstrap/Table';
import Navigation from './Navigation'
import EditProperty from './EditProperty';
import NewProperty from './NewProperty';
import {useAuthHeader} from 'react-auth-kit'
import { useNavigate } from 'react-router-dom';

function Tenants() {
  const authHeader = useAuthHeader()
  const navigate = useNavigate()
  let [tenants, setTenants] = useState([])

  let options = {
    headers: {
      'Content-Type': 'application/json',
      "Authorization": `${authHeader()}`
    }
  }

  useEffect(() => {
    fetch('http://127.0.0.1:5559/tenants', options)
      .then(res => {
        if(!res.ok){
          navigate('/login')
        }
        return res.json()
      })
      .then((data) => {
        console.log(data)
        setTenants(data)
      })
  }, [])

  return (
    <>
      <Navigation />
      <div className='container'>
        <p className='section-title'>tenants</p>
        {/* <NewProperty /> */}
        <div className='settings'>
          <Table responsive striped hover>
            <thead>
              <tr>
                <th className='py-3'>#</th>
                <th className='py-3'>First name</th>
                <th className='py-3'>Last name</th>
                <th className='py-3'>Email</th>
                <th className='py-3'></th>
              </tr>
            </thead>
            <tbody>
              {tenants.map((tenant, index) => {
                return (
                  <tr key={tenant.id}>
                    <td className='py-3'>{index+1}</td>
                    <td className='py-3'>{tenant.first_name}</td>
                    <td className='py-3'>{tenant.last_name}</td>
                    <td className='py-3'>{tenant.email}</td>
                    <td>
                      {/* <EditProperty /> */}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </Table>
        </div>
      </div>
    </>
  )
}

export default Tenants