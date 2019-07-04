import React, { Component } from 'react'

export class SideDS extends Component {
    render() {
        const  {ds,name} = this.props
        
        
        return (
            <div >
                <h5>{name}</h5><br/>            
            </div>
        )
    }
}

export default SideDS
