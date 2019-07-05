import React, { Component } from 'react'
import { Consumer } from '../context';
import FormDS from './FormDS';
import SideDS from './SideDS';

export class DataSource extends Component {

    state = {
        selected:null
    }


    render() {
        return (
            <Consumer>
                {value => {
                    const { data_sources } =value
                    if( Object.keys(data_sources).length === 0 ){
                        return(<h1>Loading</h1>)
                    }                
                    else{
                        const ds_names = Object.keys(data_sources)
                        return(
                            <div className='container-fluid'>
                            <div className='row'>
                                <div className='col-9'>
                                    <FormDS selected = {this.state.selected} />

                                </div>
                                <div className='col'>
                                {ds_names.map( ds =>(
                                    <SideDS key={ds}  ds = { data_sources[ds] } name = {ds}/>
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

export default DataSource
