import React, { Component } from 'react'

export class SideVar extends Component {
    render() {
        const  {variable,name} = this.props
        
        console.log(variable)
        console.log(name)
        return (
            <div >
                <h5>{name}</h5><br/>            
            </div>
        )
    }
}

export default SideVar
