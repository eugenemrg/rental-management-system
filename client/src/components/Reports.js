import React, { useEffect, useState } from 'react'
import './Base.css'
import Table from 'react-bootstrap/Table';
import Navigation from './Navigation'
import EditProperty from './EditProperty';
import NewProperty from './NewProperty';
import {useAuthHeader} from 'react-auth-kit'
import { useNavigate } from 'react-router-dom';

function Reports() {
  const authHeader = useAuthHeader()
  const navigate = useNavigate()
  let [issues, setIssues] = useState([])

  let options = {
    headers: {
      'Content-Type': 'application/json',
      "Authorization": `${authHeader()}`
    }
  }

  useEffect(() => {
    fetch('http://127.0.0.1:5559/issues', options)
      .then(res => {
        if(!res.ok){
          navigate('/login')
        }
        return res.json()
      })
      .then((data) => {
        console.log(data)
        setIssues(data)
      })
  }, [])

  return (
    <>
      <Navigation />
      <div className='container'>
        <p className='section-title'>issues</p>
        {/* <NewProperty /> */}
        <div className='settings'>
          <Table responsive striped hover>
            <thead>
              <tr>
                <th className='py-3'>#</th>
                <th className='py-3'>Property</th>
                <th className='py-3'>House/Unit</th>
                <th className='py-3'>Issue</th>
                <th className='py-3'>Details</th>
                <th className='py-3'>Status</th>
                <th className='py-3'></th>
              </tr>
            </thead>
            <tbody>
              {issues.map((issue, index) => {
                return (
                  <tr key={issue.id}>
                    <td className='py-3'>{index+1}</td>
                    <td className='py-3'>{issue.house.property.name}</td>
                    <td className='py-3'>{issue.house.unit}</td>
                    <td className='py-3'>{issue.issue.name}</td>
                    <td className='py-3'>{issue.detail}</td>
                    <td className='py-3'>{(issue.status === 'not fixed' ? 'Resolved' : 'Unresolved')}</td>
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

export default Reports