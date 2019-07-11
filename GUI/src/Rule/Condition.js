import React, { Component } from 'react'
import {Form,Row,Col,Button} from'react-bootstrap'


export class Condition extends Component {
    
    state = {

    }
    
    render() {
        return (
            <React.Fragment>
                <SubCond variables={this.props.variables}/>
            </React.Fragment>
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
                        <Form.Label>Select first variable</Form.Label>
                        <Form.Control as='select'>
                            {
                                var_list.map(ele => <option value={ele}>{ele}</option>)
                            }
                        </Form.Control></Form.Group>
                   
                        <Form.Label>Select operator</Form.Label>
                        <Form.Control as='select'>
                            <option value='greater_than'>greater than</option>
                            <option value='less_than'>less than</option>
                            <option value='equal_to'>equal to</option>

                        </Form.Control>
                        
                 
                    <Form.Control as='select'>
                        {
                            var_list.map(ele => <option value={ele}>{ele}</option>)
                        }
                    </Form.Control>
                
                        <Form.Control type='text' placeholder='value' ></Form.Control>
                    
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
                <Col sm={3}>
                    <Button variant = 'outline-dark' onClick={this.addCondition}>Add Condition</Button>
                </Col>
                <Col sm={5}>
                    <Button variant = 'outline-dark' onClick={this.addSubCondition}>Add Sub-Condition</Button>

                </Col>
                </Row>
                <Row>
                    <Col sm={3}>
                    </Col>
                    <Col sm={3}>
                        <CondVar variables ={this.props.variables}/>
                    </Col>
                </Row>
            </React.Fragment>
        )
    }
}