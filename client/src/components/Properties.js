import React, { useEffect, useState } from 'react'
import './Base.css'
import Table from 'react-bootstrap/Table';
import Navigation from './Navigation'
import EditProperty from './EditProperty';
import NewProperty from './NewProperty';

function Properties() {
  let [tenants, setTenants] = useState([])

  useEffect(() => {
    fetch('http://127.0.0.1:3015/tenants')
      .then(res => res.json())
      .then((data) => {
        console.log(data)
        setTenants(data)
      })
  }, [])

  return (
    <>
      <Navigation />
      <div className='container'>
        <p className='section-title'>properties</p>
        <NewProperty />
        <div className='settings'>
          <Table responsive striped hover>
            <thead>
              <tr>
                <th className='py-3'>#</th>
                <th className='py-3'>Name</th>
                <th className='py-3'>Phone</th>
                <th className='py-3'>Email</th>
                <th className='py-3'>Due Date</th>
                <th className='py-3'>Property</th>
                <th className='py-3'></th>
              </tr>
            </thead>
            <tbody>
              {tenants.map((tenant) => {
                return (
                  <tr key={tenant.id}>
                    <td className='py-3'>{tenant.id}</td>
                    <td className='py-3'>{tenant.name}</td>
                    <td className='py-3'>{tenant.phone}</td>
                    <td className='py-3'>{tenant.email}</td>
                    <td className='py-3'>{tenant.due_date}</td>
                    <td className='py-3'>{tenant.property_id}</td>
                    <td>
                      <EditProperty />
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

export default Properties