import React, { Component } from 'react'
import {Link} from 'react-router-dom'
import {ListGroup} from 'react-bootstrap'

export class SideDS extends Component {
    render(){
        const ds_names = Object.keys(this.props.data_sources)
        return(
            <React.Fragment>
            <h3>List of Data Sources</h3>
            <ListGroup>
                { ds_names.map( ds =>  <SDS key={ds}  name={ds} />)  }
            </ListGroup>
            </React.Fragment>
        )
    }
}


class SDS extends Component{
    render() {
        return (
            
                <ListGroup.Item><Link to= {'/DataSource/'+this.props.name}>{this.props.name}</Link></ListGroup.Item>
           
        )
    }
}

export default SideDS
