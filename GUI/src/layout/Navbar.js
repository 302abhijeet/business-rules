import React from 'react'
import {NavLink} from 'react-router-dom'

export default function Navbar() {
    return (
        <div className='Navigation'>
            <NavLink to ="/rule">Rule</NavLink> 
            <NavLink to ="/usecase">Use Case</NavLink>
            <NavLink to ="/variable">Variable</NavLink>
            <NavLink to ="/action">Action</NavLink>
            <NavLink to ="/datasource">Data Source</NavLink>
            <span>Viasat Inc.</span>
        </div>
    )
}
