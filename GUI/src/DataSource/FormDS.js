import React, { Component } from 'react'
import {Form,Row, Col,Button} from 'react-bootstrap'
import {Link} from 'react-router-dom'
export class FormDS extends Component {
    
    state = {
        name:'',
        method:'',
        info:{
            host_name:'',
                    user_name:'',
                    password:null,
                    key_filename:''
        },
        variables:[],
        multi_thread:true
    }
    
    componentWillMount =()=>{
        const {cat,data} = this.props
        if(cat !== 'add'){
            const {method,variables,multi_thread} = data[cat]
            this.setState({
                    name:cat,
                    method,
                    variables,
                    multi_thread
                })
                if(method === 'API'){
                    const {params,request,url} =data[cat]
                    const dat = request==='post'?data[cat]['data']:null
                    const info = {params,request,url,data:dat}
                    this.setState({info})
                }
                else if(method ==='data_base'){
                    const {host_name,user_name,password,data_base} = data[cat]
                    const info = {host_name,user_name,password,data_base}
                    this.setState({info})
                }else if(method === 'SSH'){
                    const {host_name,user_name,password,key_filename} = data[cat]
                    const info = {host_name,user_name,password,key_filename}
                    this.setState({info})
                }
    }}
    componentWillReceiveProps= (nextProps)=>{
        
        if(nextProps!==this.props && nextProps.cat !== 'add'){

            const {cat,data} = nextProps
            const {method,variables,multi_thread} = data[cat]
            this.setState({
                    name:cat,
                    method,
                    variables,
                    multi_thread
                })
                if(method === 'API'){
                    const {params,request,url} =data[cat]
                    const dat = request==='post'?data[cat]['data']:null
                    const info = {params,request,url,data:dat}
                    this.setState({info})
                }
                else if(method ==='data_base'){
                    const {host_name,user_name,password,data_base} = data[cat]
                    const info = {host_name,user_name,password,data_base}
                    this.setState({info})
                }else if(method === 'SSH'){
                    const {host_name,user_name,password,key_filename} = data[cat]
                    const info = {host_name,user_name,password,key_filename}
                    this.setState({info})
                }
            
        }
        
    }

    changeSelectState = event =>{
        this.setState({[event.target.name]:event.target.value})
        const val = event.target.value
        if(val === 'SSH'){
            this.setState({
                info:{
                    host_name:'',
                    user_name:'',
                    password:null,
                    key_filename:''
                }
            })
        }
        else if(val === 'API'){
            this.setState({
                info:{
                    request:'',
                    url:'',
                    params:{},
                    data:''
                }
            })
        }
        else if(val === 'data_base'){
            this.setState({
                info:{
                    host_name:'',
                    user_name:'',
                    password:null,
                    data_base:''
                }
            })
        }
    }

    changeState = event =>{
        this.setState({[event.target.name]:event.target.value})
    }

    changeInfoState = event =>{
        let information = this.state.info
        information[event.target.name] = event.target.value
        console.log(information)
        this.setState({info:information})
    }
    
    
    render() {
        let displaySubForm
            if(this.state.method === 'SSH'){
                 displaySubForm =  <FormDSSSH changeInfoState={this.changeInfoState} readOnly={this.props.readOnly} values = {this.state.info} />
            }else if(this.state.method === 'data_base'){
                 displaySubForm = <FormDSDB changeInfoState={this.changeInfoState} readOnly={this.props.readOnly} values = {this.state.info}/>
            }else if(this.state.method === 'API'){
                displaySubForm = <FormDSAPI changeInfoState={this.changeInfoState} readOnly={this.props.readOnly} values = {this.state.info}/>
            }
            
        
        return (
            
            
            <React.Fragment>

                {
                    this.props.cat ==='add' ? <h1>Add new Data Source</h1> : <h1>{this.props.cat} Data Source</h1>
                }
                <Form>
                    <Form.Group as={Row} controlId='name'>
                        <Form.Label column sm={3}>Name</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='name' onChange={this.changeState} readOnly={this.props.readOnly} value={this.state.name} />
                        </Col>
                    </Form.Group>
                    
                
                    <Form.Group as={Row} controlId='method'>
                        <Form.Label column sm={3}>Method</Form.Label>
                        <Col sm={9}>
                            <Form.Control as='select' name='method' onChange={this.changeSelectState} disabled={this.props.readOnly} value={this.state.method}>
                                <option value='SSH'>SSH</option>
                                <option value='data_base'>Database</option>
                                <option value='API'>API</option>
                            </Form.Control>
                        </Col>
                    </Form.Group>

                    <h5>Information regarding method:</h5>
                   
                    {displaySubForm}


                </Form>

            </React.Fragment>
        )
    }
}

export default FormDS


// Sub forms here

class FormDSSSH extends Component {
    render() {
        return (
            <React.Fragment>
            <Form.Group as={Row} controlId='host_name'>
                <Form.Label column sm={3}>Host Name</Form.Label>
                <Col sm={9}>
                    <Form.Control type='text' name='host_name' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.host_name} />
                </Col>
            </Form.Group>

            <Form.Group as={Row} controlId='user_name'>
                <Form.Label column sm={3}>Username</Form.Label>
                <Col sm={9}>
                    <Form.Control type='text' name='user_name' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.user_name}/>
                </Col>
            </Form.Group>

            <Form.Group as={Row} controlId='password'>
                <Form.Label column sm={3}>Password</Form.Label>
                <Col sm={9}>
                    <Form.Control type='password' name='password' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.password}/>
                </Col>
            </Form.Group>

            <Form.Group as={Row} controlId='key_filename'>
                <Form.Label column sm={3}>Key File Name</Form.Label>
                <Col sm={9}>
                    <Form.Control type='text' name='key_filename' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.key_filename}/>
                </Col>
            </Form.Group>

            </React.Fragment>
        )
    }
}


export class FormDSDB extends Component {
    render() {
        return (
            <React.Fragment>
            <Form.Group as={Row} controlId='host_name'>
                <Form.Label column sm={3}>Host Name</Form.Label>
                <Col sm={9}>
                    <Form.Control type='text' name='host_name' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.host_name} />
                </Col>
            </Form.Group>

            <Form.Group as={Row} controlId='user_name'>
                <Form.Label column sm={3}>Username</Form.Label>
                <Col sm={9}>
                    <Form.Control type='text' name='user_name' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.user_name}/>
                </Col>
            </Form.Group>

            <Form.Group as={Row} controlId='password'>
                <Form.Label column sm={3}>Password</Form.Label>
                <Col sm={9}>
                    <Form.Control type='password' name='password' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.password}/>
                </Col>
            </Form.Group>

            <Form.Group as={Row} controlId='data_base'>
                <Form.Label column sm={3}>Database</Form.Label>
                <Col sm={9}>
                    <Form.Control type='text' name='data_base' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.data_base}/>
                </Col>
            </Form.Group>

            </React.Fragment>
        )
    }
}


export class FormDSAPI extends Component {
    render() {
        let displayData= ''
        const {params,data} = this.props.values
        if(this.props.values.request === 'post')
            displayData =  <FormDSAPIhelper id='data' />
        return (
            <React.Fragment>

                    <Form.Group as={Row} controlId='request'>
                        <Form.Label column sm={3}>Request</Form.Label>
                        <Col sm={9}>
                            <Form.Control as='select' name='request' onChange={this.props.changeInfoState} disabled={this.props.readOnly} value={this.props.values.request}>
                                <option value='post'>Post</option>
                                <option value='get'>Get</option>
                            </Form.Control>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='url'>
                        <Form.Label column sm={3}>URL</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='url' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.url}/>
                        </Col>
                    </Form.Group>
                    {displayData}

                
                
            
            
            </React.Fragment>



        )
    }
}


export class FormDSAPIhelper extends Component {
    state = {}
    componentWillMount=()=>{
        if(this.props.datas!=null || this.props.datas!==undefined){
            this.setState({state:this.props.datas})
        }
    }
    addNewData = ()=>{
        //start here
    }
    render() {
        const {id} =this.props
        return (
            <React.Fragment>
                <Form.Group controlId={id}>
                    <Form.Label><Button variant = 'outline-dark' onClick={this.addNewData}>Add new {id}</Button></Form.Label>
                    
                </Form.Group>
            </React.Fragment>
        )
    }
}










