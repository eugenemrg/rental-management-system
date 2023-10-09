import React, { useEffect, useState } from 'react'
import './Base.css'
import Table from 'react-bootstrap/Table';
import Navigation from './Navigation'
import EditProperty from './EditProperty';
import NewProperty from './NewProperty';
import {useAuthHeader} from 'react-auth-kit'
import { useNavigate } from 'react-router-dom';

function Properties() {
  const authHeader = useAuthHeader()
  const navigate =  useNavigate()
  let [properties, setProperties] = useState([])

  let options = {
    headers: {
      'Content-Type': 'application/json',
      "Authorization": `${authHeader()}`
    }
  }

  useEffect(() => {
    fetch('http://127.0.0.1:5559/properties', options)
      .then(res => {
        if(!res.ok){
          navigate('/login')
        }
        return res.json()
      })
      .then((data) => {
        console.log(data)
        setProperties(data.properties)
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
                <th className='py-3'>Location</th>
                <th className='py-3'>Houses</th>
                <th className='py-3'></th>
              </tr>
            </thead>
            <tbody>
              {properties.map((property, index) => {
                return (
                  <tr key={property.id}>
                    <td className='py-3'>{index+1}</td>
                    <td className='py-3'>{property.name}</td>
                    <td className='py-3'>{property.location}</td>
                    <td className='py-3'>{property.houses.length}</td>
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