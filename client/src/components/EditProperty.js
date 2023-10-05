import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import './Base.css'

function NewProperty() {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      {/* <Button variant="primary" onClick={handleShow}>
        Edit
      </Button> */}
      <span className='table-icon-button' onClick={handleShow}>Edit</span>

      <Modal show={show} onHide={handleClose} centered>
        <Modal.Header closeButton>
          <Modal.Title>Edit Property Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>Property Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="e.g. Ngong Lane Apartment"
                autoFocus
              />
              <Form.Label className="mt-3">Property Location</Form.Label>
              <Form.Control
                type="text"
                placeholder="e.g. Kilimani"
                autoFocus
              />
              <Form.Label className="mt-3">Property Type</Form.Label>
              <Form.Select aria-label="Default select example">
                <option>Property Type</option>
                <option value="1">Apartment</option>
                <option value="2">Single-family home</option>
                <option value="3">Townhouse</option>
              </Form.Select>
            </Form.Group>
            {/* <Form.Group
              className="mb-3"
              controlId="exampleForm.ControlTextarea1"
            >
              <Form.Label>Example textarea</Form.Label>
              <Form.Control as="textarea" rows={3} />
            </Form.Group> */}
          </Form>
        </Modal.Body>
        <Modal.Footer>
          {/* <Button variant="secondary" onClick={handleClose}>
            Close
          </Button> */}
          <span className='table-button' onClick={handleClose}>Update</span>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default NewProperty;