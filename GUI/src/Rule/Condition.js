import React, { Component } from 'react'
import {Form,Row,Col,Button} from'react-bootstrap'


export class Condition extends Component {
    
    state = {

    }
    
    render() {
        return (
        
            <SubCond variables={this.props.variables}/>
        )
    }
}

export default Condition



class CondVar extends Component {
    state={
        name:[],
        operator:'greater_than',
        value:undefined
    }

    render() {
        const var_list = this.props.variables.map(ele => ele['name'])
        return(
            
            <React.Fragment>
               
                <Form.Group as={Row}>
                    <Form.Label>select variable</Form.Label>
                </Form.Group>
                
            </React.Fragment>
        )
    }
}


class SubCond extends Component {
    

    state={
        conditions:{},
        sub_cond:[]
    }

    addCondition=()=>{

    }
    addSubCondition=()=>{

    }

    render() {
        return(
            <React.Fragment>
                <Row>
                <Col sm={3}>
                    <Form.Control as = 'select' >
                        <option value='all'>all</option>
                        <option value='any'>any</option>
                    </Form.Control>
                </Col>
                <Col sm={4}>
                    <Button variant = 'outline-dark' onClick={this.addCondition}>Add Condition</Button>
                </Col>
                <Col sm={5}>
                    <Button variant = 'outline-dark' onClick={this.addSubCondition}>Add Sub-Condition</Button>

                </Col>    
               </Row>
               <Row>
               <CondVar variables ={this.props.variables}/>
               </Row>
               
            </React.Fragment>
        )
    }
}