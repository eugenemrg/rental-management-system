import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import {useAuthHeader} from 'react-auth-kit'
import { useNavigate } from 'react-router-dom';
import './Base.css'

function EditProperty({property: {id, name, location}, updateProperty}) {
  const authHeader = useAuthHeader()
  const navigate = useNavigate()
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const [pName, setName] = useState(name)
  const [pLocation, setLocation] = useState(location)

  function handleSubmit(e) {
    e.preventDefault()
    handleClose()

    let updated_property = {
      name: pName,
      location: pLocation
    }

    let options = {
      method: "PATCH",
      headers: {
        'Content-Type': 'application/json',
        "Authorization": `${authHeader()}`
      },
      body: JSON.stringify(updated_property)
    }

    fetch(`https://rmt-5zqu.onrender.com/properties/${id}`, options)
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
        updateProperty(data)
      })

  }

  return (
    <>
      <span className='table-icon-button' onClick={handleShow}>Edit</span>

      <Modal show={show} onHide={handleClose} centered>
        <Modal.Header closeButton>
          <Modal.Title>Edit Property Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>Property Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="e.g. Ngong Lane Apartment"
                autoFocus
                value={pName}
                onChange={e => setName(e.target.value)}
              />
              <Form.Label className="mt-3">Property Location</Form.Label>
              <Form.Control
                type="text"
                placeholder="e.g. Kilimani"
                autoFocus
                value={pLocation}
                onChange={e => setLocation(e.target.value)}
              />
            </Form.Group>
            <input type='submit' className='table-button my-2' value='Update' />
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
}

export default EditProperty;