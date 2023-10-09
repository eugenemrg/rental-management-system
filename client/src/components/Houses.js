import React, { useEffect, useState } from 'react'
import './Base.css'
import Table from 'react-bootstrap/Table';
import Navigation from './Navigation'
import EditProperty from './EditProperty';
import NewHouse from './NewHouse';
import {useAuthHeader} from 'react-auth-kit'
import { useNavigate } from "react-router-dom";

function Houses() {
  const authHeader = useAuthHeader()
  const navigate = useNavigate()
  let [houses, setHouses] = useState([])

  let options = {
    headers: {
      'Content-Type': 'application/json',
      "Authorization": `${authHeader()}`
    }
  }

  useEffect(() => {
    fetch('https://rmt-5zqu.onrender.com/houses', options)
      .then(res =>{ 
        if(!res.ok){
          navigate('/login')
        }
        return res.json()
      })
      .then((data) => {
        console.log(data)
        setHouses(data)
      })
  }, [])

  function addNewHouse(house) {
    setHouses(current => [...current, house])
  }

  return (
    <>
      <Navigation />
      <div className='container'>
        <p className='section-title'>houses</p>
        <NewHouse addHouse = {addNewHouse}/>
        <div className='settings'>
          <Table responsive striped hover>
            <thead>
              <tr>
                <th className='py-3'>#</th>
                <th className='py-3'>Unit</th>
                <th className='py-3'>Property</th>
                <th className='py-3'>Location</th>
                <th className='py-3'>Tenancy</th>
                <th className='py-3'>Tenant</th>
                <th className='py-3'></th>
              </tr>
            </thead>
            <tbody>
              {houses.map((house, index) => {
                return (
                  <tr key={house.id}>
                    <td className='py-3'>{index+1}</td>
                    <td className='py-3'>{house.unit}</td>
                    <td className='py-3'>{house.property.name}</td>
                    <td className='py-3'>{house.property.location}</td>
                    <td className='py-3'>{house.tenant != null ? 'Occupied' : 'Unoccupied'}</td>
                    <td className='py-3'>{house.tenant != null ? `${house.tenant.first_name} ${house.tenant.last_name} (${house.tenant.email})` : 'Unoccupied'}</td>
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

export default Houses