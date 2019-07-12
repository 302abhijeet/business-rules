import React, { Component } from 'react'
import {Form,Row,Col, Button} from 'react-bootstrap';
import Select from 'react-select'
import {Link} from 'react-router-dom'
import Condition from './Condition';

export class FormRule extends Component {
    
    state = {
        name:'',
        conditions:{},
        actions_true:[],
        actions_false:[],
        variables:[],
        actions:[],
        multi_thread:false,
        read:false,
        current_act_true:undefined,
        current_param_true:{},
        current_mt_true:false
    }
    
    componentWillMount = () =>{
        const {cat,rule} = this.props
        if(cat!=='add'){
            const r = rule.filter(ele => ele['name'] === cat)[0]
            console.log(r)
            
            this.setState({...r,read:true, current_act_true:undefined,current_param_true:{}})
        }else{
            this.setState({
                name:'',
                conditions:{},
                actions_true:[],
                actions_false:[],
                variables:[],
                actions:[],
                multi_thread:false,
                read:false,
                current_act_true:undefined,
                current_param_true:{}
            })
        }
    }

    componentWillReceiveProps = nextProps =>{
        if(nextProps!==this.props){
            const {cat,rule} = nextProps
            if(cat!=='add'){
                const r = rule.filter(ele => ele['name'] === cat)[0]
                

                this.setState({...r,read:true,current_act_true:undefined,current_param_true:{}})
            }else{
                this.setState({
                    name:'',
                    conditions:{},
                    actions_true:[],
                    actions_false:[],
                    variables:[],
                    actions:[],
                    multi_thread:false,
                    read:false,
                    current_act_true:undefined,
                    current_param_true:{}

                })
            }
        }
    }

    changeState= event =>{
        
        this.setState({[event.target.name]:event.target.value})
    }
    
    changeVars = (values) =>{
         
        this.setState({
            variables:values === null?[]:values.map(ele => ele['label'])
        })
    }
    changeActs = (values) =>{
        this.setState({
            actions:values===null?[]:values.map(ele => ele['label'])
        })
    }
    
    onChangeAct = event =>{
        const val = event.target.value
        const params = this.props.actions.filter(
            ele => ele['name'] === val 
        )[0]['params']
        console.log(params)

        this.setState({
            current_act_true:val,
            current_param_true: params 
        })
        this.forceUpdate()
    }

    addTrueAct = () =>{

    }
    
    render() {


        const {variables,actions} = this.props
        const var_options = variables.map(ele => {
            return {
                'value':ele['name'],
                'label':ele['name']
            }
        })
        const act_options = actions.map(ele => {
            return {
                'value':ele['name'],
                'label':ele['name']
            }
        })
        
        const cpt = this.state.current_param_true

        return (
            <React.Fragment>
                <Form>
                    {
                        this.props.cat ==='add' ? <h1>Add new Rule</h1> : <h1>{this.props.cat} Rule</h1>
                    } 
                    
                    <Form.Group as={Row} controlId='name'>
                        <Form.Label column sm={3}>Name</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='name' onChange={this.changeState} readOnly={this.state.read} value={this.state.name} />
                        </Col>
                    
                    </Form.Group>

                    <Form.Group as={Row} controlId='variables'>
                        <Form.Label column sm={3}>Variables</Form.Label>
                        <Col sm={6}>
                            <Select value={this.state.variables.map(ele => {
                                return {
                                    'value':ele,
                                    'label':ele
                                }
                            })} options={var_options} onChange={this.changeVars} name='variables' isMulti isDisabled={this.state.read}/>
                        </Col>
                        <Col>
                        <Link to='/Variable/add'>
                            <Button variant='outline-dark' disabled={this.state.read}   >Add new Variable</Button>
                            </Link>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='actions'>
                        <Form.Label column sm={3}>Actions</Form.Label>
                        <Col sm={6}>
                            <Select value={this.state.actions.map(ele => {
                                return {
                                    'value':ele,
                                    'label':ele
                                }
                            })} options={act_options} onChange={this.changeActs} name='actions' isMulti isDisabled={this.state.read}/>
                        </Col>
                        <Col>
                        <Link to='/Action/add'>
                            <Button variant='outline-dark' disabled={this.state.read}   >Add new Action</Button>
                            </Link>                        </Col>
                    </Form.Group>
                    
                    <Form.Group as={Row} controlId='conditions'>
                        <Form.Label column sm={3}>Conditions</Form.Label>
                            

                           {/* <Condition variables = {this.state.variables}/> */}
                    
                    </Form.Group>
                    
                    <Form.Group as={Row} controlId='actions_trues'>
                        <Form.Label column sm={3}>True actions</Form.Label>
                            
                        <Col sm={4}>
                            <Col>
                            <Form.Control as='select' onChange={this.onChangeAct} value = {this.state.current_act_true}>
                                { this.state.actions.map( ele => <option value={ele}>{ele}</option>     )  }
                            </Form.Control></Col>
                            <Col>
                            <Form.Label>multi_thread</Form.Label>
                            <Form.Control type='checkbox' />
                            </Col>

                        </Col>
                        <Col sm={4}>
                            <Button variant='outline-danger' onClick={this.addTrueAct}>Add this action for true</Button>
                        </Col>
                        <Row>
                            {
                                Object.keys(cpt).map( ele =>{
                                    return(
                                        <React.Fragment>
                                            <Form.Label >{ele}</Form.Label>
                                            <Form.Control type='text'></Form.Control>
                                        </React.Fragment>
                                    )
                                })
                            }
                        </Row>

                    </Form.Group>

                    

                </Form>
                
            </React.Fragment>
        )
    }
}

export default FormRule

class ActionDisplay extends Component {
    render(){
        return(
            <React.Fragment>
                <Row>
                    <Col sm={3}>
                    <Form.Group as={Row} >
                        <Form.Label column sm={3}>Name</Form.Label>
                        <Form.Control as='select' >
                            {this.props.action_list.map(
                                ele => <option value={ele}>{ele}</option>
                            )}
                        </Form.Control>
                    </Form.Group>
                    </Col>
                    <Col sm={3}>

                    </Col>
                </Row>
                

            </React.Fragment>
        )
    }
}