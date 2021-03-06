import React, { Component } from 'react'
import {Link} from 'react-router-dom'
import {ListGroup} from 'react-bootstrap'


export class SideAct extends Component {
    render(){
        const vars = this.props.actions.map( ele => ele['name'])
        return(
            <React.Fragment>
            <h3>List of Actions</h3>
            <ListGroup>
                { vars.map( ds =>  <SDS key={ds}  name={ds} />)  }
            </ListGroup>
            </React.Fragment>
        )
    }
}


class SDS extends Component{
    render() {
        return (
            
                <ListGroup.Item><Link to= {'/Action/'+this.props.name}>{this.props.name}</Link></ListGroup.Item>
           
        )
    }
}

export default SideAct
