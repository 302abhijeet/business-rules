import React, { Component } from 'react'
import {Consumer } from '../context'
import SideVar from './SideVar';
import FormVar from './FormVar';

export class Variable extends Component {

    state = {
        selected:''
    }

    render() {
        return (
            <Consumer>
                {value => {
                    const { variables } =value
                    if( Object.keys(variables).length === 0 ){
                        return(<h1>Loading</h1>)
                    }
                    else{
                        const var_names = Object.keys(variables)
                        console.log(var_names)
                        return(
                            
                                <div className='container-fluid'>
                                <div className='row'>
                                    <div className='col-9'>
                                        <FormVar selected= {this.state.selected}/>

                                    </div>
                                    <div className='col'>
                                    {var_names.map( variable =>(
                                        <SideVar key={variable}  variable = { variables[variable] } name = {variable}/>
                                    ))}

                                    </div>
                                </div>
                                
                               
                                </div>
                            
                        )
                    }
                    
                }}
            </Consumer>
        )
    }
}

export default Variable
