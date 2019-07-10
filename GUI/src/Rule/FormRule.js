import React, { Component } from 'react'
import {Form,Row,Col} from 'react-bootstrap';
import Select from 'react-select'

export class FormRule extends Component {
    
    state = {
        name:'',
        conditions:{},
        actions_true:[],
        actions_false:[],
        variables:[],
        actions:[],
        multi_thread:false,
        read:false
    }
    
    componentWillMount = () =>{
        const {cat,rule} = this.props
        if(cat!=='add'){
            const r = rule.filter(ele => ele['name'] === cat)[0]
            this.setState({...r,read:true})
        }else{
            this.setState({
                name:'',
                conditions:{},
                actions_true:[],
                actions_false:[],
                variables:[],
                actions:[],
                multi_thread:false,
                read:false
            })
        }
    }

    componentWillReceiveProps = nextProps =>{
        if(nextProps!==this.props){
            const {cat,rule} = this.props
            if(cat!=='add'){
                const r = rule.filter(ele => ele['name'] === cat)[0]
                this.setState({...r,read:true})
            }else{
                this.setState({
                    name:'',
                    conditions:{},
                    actions_true:[],
                    actions_false:[],
                    variables:[],
                    actions:[],
                    multi_thread:false,
                    read:false
                })
            }
        }
    }

    changeState= event =>{
        this.setState({[event.target.name]:event.target.value})
    }
    // changeVars = (event) =>{
    //     this.setState({
    //         variables:event.target.value
    //     })
    // }
    
    
    render() {


        const {variables} = this.props
        const var_options = variables.map(ele => {
            return {
                'value':ele['name'],
                'label':ele['name']
            }
        })
        

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
                        <Col sm={9}>
                            <Select value={this.state.variables} options={var_options} onChange={this.changeState} name='variables' isMulti isDisabled={this.state.read}/>
                        </Col>
                    </Form.Group>


                </Form>
                
            </React.Fragment>
        )
    }
}

export default FormRule
