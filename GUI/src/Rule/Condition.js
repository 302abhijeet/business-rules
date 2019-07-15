import React, { Component } from 'react'
import {Form,Row,Col,Button} from'react-bootstrap'


export class Condition extends Component {
    
    state = {
        data_tree:{}
    }
    
    render() {
        return (
            <React.Fragment>
                <Form.Group>
                    <Form.Label>Conditions</Form.Label>
                    <SubCond variables={this.props.variables} data_tree = {this.state.data_tree}/> 
                </Form.Group>
                

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
                <Form.Group>
                    <Form.Label column sm={3}></Form.Label>
                </Form.Group>
               
            </React.Fragment>
        )
    }
}