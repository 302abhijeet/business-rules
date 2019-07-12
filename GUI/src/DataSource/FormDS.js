import React, { Component } from 'react'
import {Form,Row, Col,Button,ButtonGroup,ToggleButton} from 'react-bootstrap'

export class FormDS extends Component {
    
    state = {
        name:'',
        method:'',
        info:{
            host_name:'',
            user_name:'',
            password:'',
            key_filename:''
        },
        variables:[],
        multi_thread:true,
        read:false
    }
    

    componentWillMount = ()=>{
        const {cat,data} = this.props
        if(cat!=='add'){
            const d = data.filter(ele  => ele['name'] === cat)[0]
            const {name,method,variables,multi_thread} = d
            this.setState({name,method,variables,multi_thread,read:true})
            if(method==='API'){
                const {params,request,url} = d
                const dat = request==='post'?d['data']:null
                const info = {params,request,url,data:dat}
                this.setState({info})
            }
            else if(method ==='data_base'){
                const {host_name,user_name,password,data_base} = d
                const info = {host_name,user_name,password,data_base}
                this.setState({info})
            }
            else if(method==='SSH'){
                const {host_name,user_name,password,key_filename} = d
                const info = {host_name,user_name,password,key_filename}
                this.setState({info})
            }
        }
    }

    componentWillReceiveProps = nextProps =>{
        if(nextProps!==this.props){
            const {cat,data} = this.props
            if(cat!=='add'){
            const d = data.filter(ele  => ele['name'] === cat)[0]
            const {name,method,variables,multi_thread} = d
            this.setState({name,method,variables,multi_thread,read:true})
            if(method==='API'){
                const {params,request,url} = d
                const dat = request==='post'?d['data']:null
                const info = {params,request,url,data:dat}
                this.setState({info})
            }
            else if(method ==='data_base'){
                const {host_name,user_name,password,data_base} = d
                const info = {host_name,user_name,password,data_base}
                this.setState({info})
            }
            else if(method==='SSH'){
                const {host_name,user_name,password,key_filename} = d
                const info = {host_name,user_name,password,key_filename}
                this.setState({info})
            }
        }
        }
    }

    // componentWillMount =()=>{
    //     const {cat,data} = this.props
    //     if(cat !== 'add'){
            
    //         const d = data.filter(ele  => ele['name'] === cat)[0]
            
            
    //         const {method,variables,multi_thread} = d[cat]
    //         this.setState({
    //                 name:cat,
    //                 method,
    //                 variables,
    //                 multi_thread
    //             })
    //             if(method === 'API'){
    //                 const {params,request,url} =d[cat]
    //                 const dat = request==='post'?d[cat]['data']:null
    //                 const info = {params,request,url,data:dat}
    //                 this.setState({info})
    //             }
    //             else if(method ==='data_base'){
    //                 const {host_name,user_name,password,data_base} = data[cat]
    //                 const info = {host_name,user_name,password,data_base}
    //                 this.setState({info})
    //             }else if(method === 'SSH'){
    //                 const {host_name,user_name,password,key_filename} = data[cat]
    //                 const info = {host_name,user_name,password,key_filename}
    //                 this.setState({info})
    //             }
    // }}
    

    // componentWillReceiveProps= (nextProps)=>{
        
    //     if(nextProps!==this.props && nextProps.cat !== 'add'){

    //         const {cat,data} = nextProps
    //         const d = data.filter(ele  => ele['name'] === cat)[0]

    //         const {method,variables,multi_thread} = d[cat]
    //         this.setState({
    //                 name:cat,
    //                 method,
    //                 variables,
    //                 multi_thread
    //             })
    //             if(method === 'API'){
    //                 const {params,request,url} =data[cat]
    //                 const dat = request==='post'?data[cat]['data']:null
    //                 const info = {params,request,url,data:dat}
    //                 this.setState({info})
    //             }
    //             else if(method ==='data_base'){
    //                 const {host_name,user_name,password,data_base} = data[cat]
    //                 const info = {host_name,user_name,password,data_base}
    //                 this.setState({info})
    //             }else if(method === 'SSH'){
    //                 const {host_name,user_name,password,key_filename} = data[cat]
    //                 const info = {host_name,user_name,password,key_filename}
    //                 this.setState({info})
    //             }
            
    //     }
        
    // }

    changeSelectState = event =>{
        this.setState({[event.target.name]:event.target.value})
        const val = event.target.value
        if(val === 'SSH'){
            this.setState({
                info:{
                    host_name:'',
                    user_name:'',
                    password:'',
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
                    data:{}
                }
            })
        }
        else if(val === 'data_base'){
            this.setState({
                info:{
                    host_name:'',
                    user_name:'',
                    password:'',
                    data_base:''
                }
            })
        }
    }

    changeDataParams = (newData,id) =>{
        let information = this.state.info
        if(id==='Parameter')
            id = 'params'
        if(id === 'Data')
            id='data'
        console.log(id)
        information[id] = newData
        console.log(information)
        this.setState({info:information})
    }

    changeState = event =>{
        this.setState({[event.target.name]:event.target.value})
    }

    changeInfoState = event =>{
        let information = this.state.info
        information[event.target.name] = event.target.value
        this.setState({info:information})
    }
    
    changeCheck = event =>{
        this.setState({[event.target.name]: !this.state.multi_thread})
    }

    submitData = (e) =>{
        e.preventDefault()
        const st = this.state
        delete st['read']
        const name = st['name']
        delete st['name']
        const newOb = {
            [name]: st
        }
        this.props.addNewData('data_sources',newOb)
    }
    changeReadMode = ()=>{
        const prev = this.state.read
        this.setState({read:!prev})
    }

    render() {
        let displaySubForm
            if(this.state.method === 'SSH'){
                 displaySubForm =  <FormDSSSH changeInfoState={this.changeInfoState} readOnly={this.state.read} values = {this.state.info} />
            }else if(this.state.method === 'data_base'){
                 displaySubForm = <FormDSDB changeInfoState={this.changeInfoState} readOnly={this.state.read} values = {this.state.info}/>
            }else if(this.state.method === 'API'){
                displaySubForm = <FormDSAPI changeInfoState={this.changeInfoState} readOnly={this.state.read} values = {this.state.info} changeDataParams={this.changeDataParams}/>
            }
            
        
        return (
            
            
            <React.Fragment>

                {
                    this.props.cat ==='add' ? <h1>Add new Data Source</h1> : <h1>{this.props.cat} Data Source</h1>
                }
                <Form onSubmit={this.submitData}>
                    <Form.Group as={Row} controlId='name'>
                        <Form.Label column sm={3}>Name</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='name' onChange={this.changeState} readOnly={this.state.read} value={this.state.name} />
                        </Col>
                    </Form.Group>
                    
                
                    <Form.Group as={Row} controlId='method'>
                        <Form.Label column sm={3}>Method</Form.Label>
                        <Col sm={9}>
                            <Form.Control as='select' name='method' onChange={this.changeSelectState} disabled={this.state.read} value={this.state.method}>
                                <option value='SSH'>SSH</option>
                                <option value='data_base'>Database</option>
                                <option value='API'>API</option>
                            </Form.Control>
                        </Col>
                    </Form.Group>

                    <h5>Information regarding method:</h5>
                   
                    {displaySubForm}

                    <Form.Group as={Row} controlId="formBasicChecbox">
                        <Form.Label column sm={3}>Multithread</Form.Label>
                        <Form.Check type="checkbox" name='multi_thread' disabled={this.state.read} value={this.state.multi_thread} onChange={this.changeCheck}/>
                    </Form.Group>

                    <Button type = 'submit' variant='outline-success' disabled={this.state.read}>Submit</Button>
                    <Button name='modify' variant='outline-secondary' disabled={!this.state.read} onClick={this.changeReadMode}>Modify</Button>
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
            displayData =  <FormDSAPIhelper id='Data' data={data} onChange={this.props.changeInfoState} readOnly= {this.props.readOnly} changeDataParams={this.props.changeDataParams}/>
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

                    <FormDSAPIhelper id='Parameter' data={params} onChange={this.props.changeInfoState} readOnly= {this.props.readOnly} changeDataParams={this.props.changeDataParams}/>
                
            
            
            </React.Fragment>



        )
    }
}


export class FormDSAPIhelper extends Component {
    
    newVal = React.createRef()
    newKey = React.createRef()
    
    state = {}
    componentWillMount=()=>{
        if(this.props.datas!==null || this.props.datas!==undefined){
            this.setState(this.props.data)
        }
    }

    addNewData = ()=>{
        console.log('newData')
        const st = this.state
        const newState = {...st,
            [this.newKey.current.value]:this.newVal.current.value
        }
        this.setState(newState)
        this.newKey.current.value=''
        this.newVal.current.value=''
        this.props.changeDataParams(newState,this.props.id)
    }

    deleteData = (e)=>{
       
        const st = this.state
        delete st[e]
        this.setState(st)
        this.props.changeDataParams(st,this.props.id)
    }

    render() {
        const {id,readOnly,data} =this.props
        return (
            <React.Fragment>
                <Form.Group controlId={id}>
                    <Row>
                        <Col sm={3}><Form.Label>{id}</Form.Label></Col>
                        <Col sm={9}>
                            {
                                Object.keys(this.state).map(ele => {
                                    return(
                                        <Row>
                                            <Col>                 
                                                <Form.Control type='text' name={ele} onChange={this.props.changeInfoState} readOnly={true} value={ele}/>

                                            </Col>
                                            <Col>                                        
                                                <Form.Control type='text' name={this.state[ele]} onChange={this.props.changeInfoState} readOnly={true} value={this.state[ele]}/>
                                            </Col>
                                            <Col>
                                                <Button variant='outline-danger' name={ele} disabled={readOnly} onClick={()=>this.deleteData(ele)}>Delete</Button>
                                            </Col>
                                        </Row>
                                    )
                                })
                            }

                        </Col>
                    </Row>
                    <Row>
                        <Col sm={3}>
                            <Form.Label><Button variant = 'outline-dark' onClick={this.addNewData} disabled={readOnly}>Add new {id}</Button></Form.Label>

                        </Col>
                        <Col><Row> 
                        <Col>               
                            <Form.Control type='text' name='newKey' onChange={this.props.changeInfoState} readOnly={readOnly} ref={this.newKey} />

                            </Col>
                            <Col>                                        
                                <Form.Control type='text' name='newVal' onChange={this.props.changeInfoState} readOnly={readOnly} ref={this.newVal}/>
                            </Col>
                            <Col></Col>
                            </Row>
                        </Col>
                        
                    
                    </Row>
                    
                </Form.Group>
            </React.Fragment>
        )
    }
}










