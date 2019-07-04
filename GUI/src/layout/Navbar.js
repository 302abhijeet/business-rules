import React from 'react'
import {NavLink} from 'react-router-dom'

export default function Navbar() {
    return (
        <nav className='navbar navbar-expand-lg navbar-light bg-light'>
                        <span className='navbar-brand'>Rule Engine</span>

            <NavLink to ="/rule" className='nav-link'>Rule</NavLink> 
            <NavLink to ="/usecase" className='nav-link'> Use Case</NavLink>
            <NavLink to ="/variable" className='nav-link'>Variable</NavLink>
            <NavLink to ="/action" className='nav-link'>Action</NavLink>
            <NavLink to ="/datasource" className='nav-link' >Data Source</NavLink>
        </nav>
    )
}
