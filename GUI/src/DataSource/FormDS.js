import React, { Component } from 'react'
import {Modal,Form,Row, Col,Button,ButtonGroup,ToggleButton} from 'react-bootstrap'
import {withRouter} from 'react-router-dom'
import { Prompt } from 'react-router'
import Select from 'react-select'

export class FormDS extends Component {
    
    state = {
        name:'',
        method:'',
        info:{},
        variables:[],
        multi_thread:true,
        cache:true,
        validated:false,
        read:false,
        show_modal:false
    }
    hasFetched = false
    shouldComponentUpdate(nextProps, nextState) {
        if (this.hasFetched){
          return false;
        }
        return true;
    }
    componentWillUpdate(nextProps, nextState) {
        if(this.props.run) {
            this.props.addData(nextState,this.props._id)
        }
    }

    componentWillMount = ()=>{
        const {cat,data_sources} = this.props
        if(cat!=='add'){
            const data = data_sources.filter(ele  => ele['name'] === cat)[0]
            const {name,method,variables,multi_thread,cache} = data
            this.setState({name,method,variables,multi_thread,cache,read:true,validated:false,show_modal:false})
            if(method==='API'){
                const {params,request,url} = data
                const info = {params,request,url,data:request==='post'?data['data']:null,key:'',value:''}
                this.setState({info})
            }
            else if(method ==='data_base'){
                const {host_name,user_name,password,data_base} = data
                const info = {host_name,user_name,password,data_base}
                this.setState({info})
            }
            else if(method==='SSH'){
                const {host_name,user_name,password,key_filename} = data
                const info = {host_name,user_name,password,key_filename}
                this.setState({info})
            }
        }
    }

    componentWillReceiveProps = nextProps =>{
        if(nextProps!==this.props){
            const {cat,data_sources} = nextProps
            if(cat!=='add'){
                const data = data_sources.filter(ele  => ele['name'] === cat)[0]
                const {name,method,variables,multi_thread,cache} = data
                this.setState({name,method,variables,multi_thread,cache,read:true,validated:false,show_modal:false})
                if(method==='API'){
                    const {params,request,url} = data
                    const dat = request==='post'?data['data']:null
                    const info = {params,request,url,data:dat}
                    this.setState({info})
                }
                else if(method ==='data_base'){
                    const {host_name,user_name,password,data_base} = data
                    const info = {host_name,user_name,password,data_base}
                    this.setState({info})
                }
                else if(method==='SSH'){
                    const {host_name,user_name,password,key_filename} = data
                    const info = {host_name,user_name,password,key_filename}
                    this.setState({info})
                }
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
                    key_filename:null
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
                    password:null,
                    data_base:null
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
    changeVars = (values) =>{
        const val=values === null?[]:values.map(ele => ele['label'])
        this.setState({
            variables:val
        })
        
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
    changeCheckCache = event =>{
        this.setState({[event.target.name]: !this.state.cache})
        
    }
    closeModal = () => {
        this.setState({show_modal:false})
    }
    showModal = () => {
        this.setState({show_modal:true})
    }
    deleteData =()=>{
        this.props.delData('DataSource',{name: this.state['name']})
        this.props.history.push('/DataSource/index')
    }

    submitData = (e) =>{
        const form = e.currentTarget
        if (form.checkValidity() === false) {
            e.preventDefault()
            e.stopPropagation()
        }
        else {
            e.preventDefault()
            console.log('submitting data')
            const data = this.state
            if(this.props.cat==='add' && this.props.data_sources.filter( ele => ele['name']===data['name']).length > 0){
                e.stopPropagation()
                this.showModal()
                return false
            }
            delete data['read']
            delete data['validated']
            delete data["show_modal"]
            Object.keys(data['info']).forEach( ele => {
                data[ele] = data["info"][ele]
            })
            delete data['info']
            console.log(data)
            if(this.props.cat==='add'){
                console.log('in add')
                this.props.addData('DataSource',data)
                if (!this.props.popUp) {
                    console.log("Why here")
                    this.props.history.push('/DataSource/index')
                }
                else {
                    console.log("yes pop up!")
                    this.hasFetched = true
                    this.props.closeDataSourceModal()
                }
                console.log("getting out add!")
            }
            else{
                console.log('in '+this.props.cat)
                let newData = {
                    querry : {name : data['name']},
                    newData : data
                }
                this.props.modifyData('DataSource',newData)
                this.props.history.push('/DataSource/index')
            }
        }
        this.setState({validated:true})
    }
    changeReadMode = ()=>{
        const prev = this.state.read
        this.setState({read:!prev})
    }

    render() {
        const {validated} = this.state
        const {variables} = this.props
        console.log(variables)
        const var_options = variables !== undefined? variables.map(ele => {
            return {
                'value':ele,
                'label':ele
            }
        }) : null
        console.log(var_options)
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
                <Prompt
                    when={!this.state.read}
                    message="Click OK to Continue! ALL data in the form will be lost!"
                />
                <Modal show={this.state.show_modal}>
                        <Modal.Header closeButton><Modal.Title>Cannot ADD DataSource</Modal.Title></Modal.Header>
                        <Modal.Body> <p>DataSource name already exists!</p></Modal.Body>
                        <Modal.Footer><Button variant="secondary" onClick={this.closeModal}>Close</Button></Modal.Footer>
                </Modal>
                <Row>
                    <Col hidden={this.props.run}>{
                        this.props.cat ==='add' ? <h1>Add new Data Source</h1> : <h1>{this.props.cat} Data Source</h1>
                    }</Col>
                    <Col md="auto"><Button name='modify' variant='outline-secondary' disabled={!this.state.read} hidden={this.props.popUp || this.props.run} onClick={this.changeReadMode}>Modify</Button></Col>
                    <Col md="auto"><Button name = 'delete' variant='outline-danger' disabled={!this.state.read} hidden={this.props.popUp || this.props.run} onClick={this.deleteData}>Delete</Button></Col>
                </Row>
                <Form className="overflow-auto" noValidate validated={validated} onSubmit={this.submitData} hidden={this.props.hidden}>
                    <Form.Group as={Row} controlId='name'>
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Name</Form.Label>
                        <Col sm={9}>
                            <Form.Control required type='text' name='name' onChange={this.changeState} readOnly={this.state.read} value={this.state.name} />
                        </Col>
                    </Form.Group>
                    
                
                    <Form.Group as={Row} controlId='method'>
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Method</Form.Label>
                        <Col sm={9}>
                            <Form.Control required as='select' name='method' onChange={this.changeSelectState} disabled={this.state.read} value={this.state.method}>
                                <option value="" selected hidden>
                                        Select an option
                                    </option>
                                <option value='SSH'>SSH</option>
                                <option value='data_base'>Database</option>
                                <option value='API'>API</option>
                            </Form.Control>
                        </Col>
                    </Form.Group>

                    <h5>Information regarding method:</h5>
                   
                    {displaySubForm}

                    <Form.Group as={Row} controlId="formBasicChecbox">
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Multithread</Form.Label>
                        <Form.Check type="checkbox" checked={this.state.multi_thread} name='multi_thread' disabled={this.state.read} value={this.state.multi_thread} onChange={this.changeCheck}/>
                    </Form.Group>

                    <Form.Group as={Row} controlId="formBasicChecbox">
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Cache</Form.Label>
                        <Form.Check type="checkbox" checked={this.state.cache} name='cache' disabled={this.state.read} value={this.state.cache} onChange={this.changeCheckCache}/>
                    </Form.Group>

                    <div hidden={!this.props.run}>
                        <Form.Group as={Row} controlId='variables'>
                            <Form.Label column sm={3}>Variables</Form.Label>
                            <Col sm={6}>
                                <Select value={this.state.variables.map(ele => {
                                    return {
                                        'value':ele,
                                        'label':ele
                                    }
                                })} options={var_options} onChange={this.changeVars} name='variables' isMulti/>
                            </Col>
                        </Form.Group>
                    </div>

                    <Row>
                        <Col md="auto"><Button hidden={this.props.run} type = 'submit' variant='outline-success' disabled={this.state.read}>Submit</Button></Col>
                    </Row>
                </Form>

            </React.Fragment>
        )
    }
}

export default withRouter(FormDS)


// Sub forms here

class FormDSSSH extends Component {
    render() {
        return (
            <React.Fragment>
            <Form.Group as={Row} controlId='host_name'>
                <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Host Name</Form.Label>
                <Col sm={9}>
                    <Form.Control required type='text' name='host_name' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.host_name} />
                </Col>
            </Form.Group>

            <Form.Group as={Row} controlId='user_name'>
                <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Username</Form.Label>
                <Col sm={9}>
                    <Form.Control type='text' required name='user_name' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.user_name}/>
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
                <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Host Name</Form.Label>
                <Col sm={9}>
                    <Form.Control required type='text' name='host_name' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.host_name} />
                </Col>
            </Form.Group>

            <Form.Group as={Row} controlId='user_name'>
                <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Username</Form.Label>
                <Col sm={9}>
                    <Form.Control required type='text' name='user_name' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.user_name}/>
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
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Request</Form.Label>
                        <Col sm={9}>
                            <Form.Control required as='select' name='request' onChange={this.props.changeInfoState} disabled={this.props.readOnly} value={this.props.values.request}>
                                <option value="" selected hidden>Select an option</option>
                                <option value='post'>Post</option>
                                <option value='get'>Get</option>
                            </Form.Control>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='url'>
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>URL</Form.Label>
                        <Col sm={9}>
                            <Form.Control required type='text' name='url' onChange={this.props.changeInfoState} readOnly={this.props.readOnly} value={this.props.values.url}/>
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
        if (this.newKey.current.value && this.newVal.current.value) {
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
        else {
            return false
        }
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
                            <Form.Control type='text' placeholder='Name' name='newKey' onChange={this.props.changeInfoState} readOnly={readOnly} ref={this.newKey} />

                            </Col>
                            <Col>                                        
                                <Form.Control type='text' placeholder='Value' name='newVal' onChange={this.props.changeInfoState} readOnly={readOnly} ref={this.newVal}/>
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










