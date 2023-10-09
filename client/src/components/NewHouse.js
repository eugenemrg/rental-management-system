import { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import { useAuthHeader } from 'react-auth-kit'
import { useNavigate } from 'react-router-dom';
import './Base.css'

function NewHouse({ addHouse }) {
    const authHeader = useAuthHeader()
    const navigate = useNavigate()
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const [unit, setUnit] = useState('')
    const [property_id, setPropertyId] = useState('1')

    const [properties, setProperties] = useState([])

    useEffect(() => {
        let options = {
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `${authHeader()}`
            }
        }

        fetch('http://127.0.0.1:5559/properties', options)
            .then(res => {
                if (!res.ok) {
                    navigate('/login')
                }
                return res.json()
            })
            .then((data) => {
                setProperties(data.properties)
            })
    }, [])

    function handleSubmit(e) {
        e.preventDefault()
        handleClose()

        let new_property = {
            unit: unit
        }

        let options = {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `${authHeader()}`
            },
            body: JSON.stringify(new_property)
        }

        fetch(`http://127.0.0.1:5559/houses/${property_id}`, options)
            .then(res => {
                if (!res.ok) {
                    navigate('/login')
                }
                return res.json()
            })
            .then((data) => {
                setUnit('')
                setPropertyId('')

                console.log(data)
                addHouse(data)
            })

    }

    return (
        <>
            <span className='main-button' onClick={handleShow}>Add New House</span>

            <Modal show={show} onHide={handleClose} centered>
                <Modal.Header closeButton>
                    <Modal.Title>New House</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                            <Form.Label>Unit Name</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="e.g. A16"
                                autoFocus
                                value={unit}
                                onChange={e => setUnit(e.target.value)}
                            />
                            <Form.Label className="mt-3">Property</Form.Label>
                            <Form.Select aria-label="Default select property" value={property_id} onChange={e => setPropertyId(e.target.value)}>
                                <option>Select Property</option>
                                {properties.map(property => {
                                    return <option value={property.id}>{property.name}</option>
                                })}
                            </Form.Select>
                        </Form.Group>
                        <input type='submit' className='table-button my-2' value='Add House' />
                    </Form>
                </Modal.Body>
            </Modal>
        </>
    );
}

export default NewHouse;