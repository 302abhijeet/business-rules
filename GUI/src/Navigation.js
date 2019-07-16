import React, { Component } from 'react'
import {Navbar,Nav} from 'react-bootstrap'
import {Link} from 'react-router-dom'

export class Navigation extends Component {
    render() {
        return (
            <Navbar bg='light' expand='lg'>
                <Link to='/'><Navbar.Brand >Rule Engine</Navbar.Brand></Link>
                <Nav className='mr-auto'>
                    <Nav.Link><Link to='/DataSource/index'>DataSource</Link></Nav.Link>
                    <Nav.Link><Link to='/Rule/index'>Rule</Link></Nav.Link>
                    <Nav.Link><Link to='/UseCase/index'>UseCase</Link></Nav.Link>
                    <Nav.Link><Link to='/Variable/index'>Variable</Link></Nav.Link>
                    <Nav.Link><Link to='/Action/index'>Action</Link></Nav.Link>
                </Nav>

            </Navbar>
        )
    }
}

export default Navigation
