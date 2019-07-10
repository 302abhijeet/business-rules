import React, { Component } from 'react'
import {Link} from 'react-router-dom'
import {ListGroup} from 'react-bootstrap'

export class SideRule extends Component {
    render(){
        const vars = this.props.rule.map( ele => ele['name'])
        return(
            <React.Fragment>
            <h3>List of Rules</h3>
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
            
                <ListGroup.Item><Link to= {'/Rule/'+this.props.name}>{this.props.name}</Link></ListGroup.Item>
           
        )
    }
}

export default SideRule
