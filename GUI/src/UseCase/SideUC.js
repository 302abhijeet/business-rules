import React, { Component } from 'react'
import {Link} from 'react-router-dom'
import {ListGroup} from 'react-bootstrap'

export class SideUC extends Component {
    render(){
        const vars = this.props.use_cases.map( ele => ele['name'])
        return(
            <React.Fragment>
            <h3>List of Variables</h3>
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
            
                <ListGroup.Item><Link to= {'/UseCase/'+this.props.name}>{this.props.name}</Link></ListGroup.Item>
           
        )
    }
}

export default SideUC
