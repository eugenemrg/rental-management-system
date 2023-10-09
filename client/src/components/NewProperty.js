import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import {useAuthHeader} from 'react-auth-kit'
import { useNavigate } from 'react-router-dom';
import './Base.css'

function NewProperty({ addProperty }) {
  const authHeader = useAuthHeader()
  const navigate = useNavigate()
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const [name, setName] = useState('')
  const [location, setLocation] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    handleClose()

    let new_property = {
      name: name,
      location: location
    }

    let options = {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        "Authorization": `${authHeader()}`
      },
      body: JSON.stringify(new_property)
    }

    fetch('https://rmt-5zqu.onrender.com/properties', options)
      .then(res => {
        if (!res.ok) {
          navigate('/login')
        }
        return res.json()
      })
      .then((data) => {
        setName('')
        setLocation('')
        
        console.log(data)
        addProperty(data)
      })

  }

  return (
    <>
      <span className='main-button' onClick={handleShow}>Add New Property</span>

      <Modal show={show} onHide={handleClose} centered>
        <Modal.Header closeButton>
          <Modal.Title>New Property</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>Property Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="e.g. Ngong Lane Apartment"
                autoFocus
                value={name}
                onChange={e => setName(e.target.value)}
              />
              <Form.Label className="mt-3">Property Location</Form.Label>
              <Form.Control
                type="text"
                placeholder="e.g. Kilimani"
                value={location}
                onChange={e => setLocation(e.target.value)}
              />
            </Form.Group>
            <input type='submit' className='table-button my-2' value='Update'/>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
}

export default NewProperty;