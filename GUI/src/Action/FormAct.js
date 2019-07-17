import React, { Component } from 'react'
import { isFor } from '@babel/types';
import {Modal,Form,Row,Col,Button, ListGroup} from 'react-bootstrap'
import {withRouter} from 'react-router-dom'
import { Prompt } from 'react-router'
export class FormAct extends Component {
    
    state={
        name:'',
        params:{},
        formulae:'',
        read:false,
        key:'',
        value:'',
        validated:false,
        show_modal:false
    } 
    
    componentWillMount = () =>{
        const {cat,actions } = this.props
        if(cat!=='add'){
            const data = actions.filter(ele => ele['name']===cat)[0]
            this.setState({...data,read:true,key:'',value:'',validated:false,show_modal:false})
        }
        else{
            this.setState({
                name:'',
                params:{},
                formulae:'',
                read:false,
                key:'',
                value:'',
                validated:false,
                show_modal:false
            })
        }
    }

    componentWillReceiveProps=(nextProps)=>{
        if(nextProps!==this.props){
            const {cat,actions } = nextProps
            if(cat!=='add'){
                const data = actions.filter(ele => ele['name']===cat)[0]
                this.setState({...data,read:true,key:'',value:'',validated:false,show_modal:false})
            }else{
                this.setState({
                    name:'',
                    params:{},
                    formulae:'',
                    read:false,
                    key:'',
                    value:'',
                    validated:false,
                    show_modal:false
                })
            }
        }
    }
    changeReadMode = () =>{
        this.setState({
            read:!this.state.read
        })
    }
    deleteData =()=>{
        this.props.delData('actions',{name: this.state['name']})
        this.props.history.push('/Action/index')
    }

    delParam = key =>{
        const p = this.state.params
        delete p[key]
        this.setState({
            params:{...p}
        })
    }

    changeState = event =>{
        this.setState(
            {
                [event.target.name]:event.target.value
            }
        )
    }

    addPara=()=>{
        if (this.state.key && this.state.value) {
            this.setState({
                params:{...this.state.params,[this.state.key]:this.state.value}
            })
        }
        else {
            return false
        }
    }

    closeModal = () => {
        this.setState({show_modal:false})
    }
    showModal = () => {
        this.setState({show_modal:true})
    }

    submitData =(e) =>{
        const form = e.currentTarget
        if (form.checkValidity() === false) {
            e.preventDefault()
            e.stopPropagation()
        }
        else {
            e.preventDefault()
            console.log('submitting data')
            const data = this.state
            delete data['read']
            delete data['key']
            delete data['value']
            delete data['validated']
            delete data["show_modal"]
            console.log(data)
            if(this.props.cat==='add'){
                console.log('in add')
                if( this.props.actions.filter( ele => ele['name']===data['name']).length > 0){
                    e.stopPropagation()
                    this.showModal()
                    return false
                }
                this.props.addData('actions',data)
                this.props.history.push('/Action/index')

            }
            else{
                console.log('in '+this.props.cat)
                let newData = {
                    querry : {name : data['name']},
                    newData : data
                }
                this.props.modifyData('actions',newData)
                this.props.history.push('/Action/index')
            }
        }
        this.setState({validated:true})
    }

    render() {
        const {validated} = this.state
        return (
            <React.Fragment>
                <Prompt
                    when={!this.state.read}
                    message="Click OK to Continue! ALL data in the form will be lost!"
                />
                <Modal show={this.state.show_modal}>
                        <Modal.Header closeButton><Modal.Title>Cannot ADD action</Modal.Title></Modal.Header>
                        <Modal.Body> <p>Action name already exists!</p></Modal.Body>
                        <Modal.Footer><Button variant="secondary" onClick={this.closeModal}>Close</Button></Modal.Footer>
                </Modal>
                <Form noValidate validated={validated} onSubmit={this.submitData}> 
                <Row>
                    <Col>{
                        this.props.cat ==='add' ? <h1>Add new Action</h1> : <h1>{this.props.cat} Action</h1>
                    }</Col>
                    <Col md="auto"><Button name='modify' variant='outline-secondary' disabled={!this.state.read} onClick={this.changeReadMode}>Modify</Button></Col>
                    <Col md="auto"><Button name = 'delete' variant='outline-danger' disabled={!this.state.read} onClick={this.deleteData}>Delete</Button></Col>   
                </Row> 

                <Form.Group as={Row} controlId='name'>
                    <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Name</Form.Label>
                    <Col sm={9}>
                        <Form.Control required type='text' name='name' onChange={this.changeState} readOnly={this.state.read} value={this.state.name} />
                        <Form.Control.Feedback type="invalid">Enter Action Name!</Form.Control.Feedback>
                    </Col>
                
                </Form.Group>
                     
                <Form.Group as={Row} controlId='params'>
                    
                    <Form.Label column sm = {3}>Parameters</Form.Label>
                   
                        <Col><Form.Control type='text' placeholder='name' name='key' onChange={this.changeState} readOnly={this.state.read} value={this.state.key} /></Col>
                        <Col>
                            <Form.Control as='select' name='value' onChange={this.changeState} disabled={this.state.read} value={this.state.value} >
                                    <option value="" selected hidden>
                                        Select an option
                                    </option>
                                    <option value = 'numeric'>
                                        numeric
                                    </option>
                                    <option value = 'text'>
                                        text
                                    </option>
                                    <option value = 'none'>
                                        no input
                                    </option>
                                    <option value = 'select'>
                                        select
                                    </option>
                                    <option value = 'select_multiple'>
                                        select_multiple
                                    </option>
                            </Form.Control>
                        </Col>
                        <Col><Button variant='outline-secondary' onClick={this.addPara}>Add Parameter</Button></Col>
                
                    
                </Form.Group> 
                <Row>
                    <Col>
                    {
                        Object.keys(this.state.params).map(ele => <ParameterDisplay key ={ele} keyv={ele} value={this.state.params[ele]} delParam={this.delParam} read={this.state.read}/>   )
                    }</Col>
                </Row>

                <Form.Group as={Row} controlId='formulae'>
                    <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Formulae</Form.Label>
                    <Col sm={9}>
                        <Form.Control required as='textarea' name='formulae' onChange={this.changeState} readOnly={this.state.read} value={this.state.formulae} />
                        <Form.Control.Feedback type="invalid">Enter formulae for what action must do!</Form.Control.Feedback>
                    </Col>
                </Form.Group>

                <Row>
                        <Col><Button type = 'submit' variant='outline-success' disabled={this.state.read}>Submit</Button></Col>
                </Row>
            </Form>

            </React.Fragment>
        )
    }
}

export default withRouter(FormAct) 

class ParameterDisplay extends Component{

    render(){
        return(
            <React.Fragment>
                <Row>
                    <Col sm={3}></Col>
                    <Col><Form.Label>{this.props.keyv}</Form.Label></Col>
                    <Col><Form.Label>{this.props.value}</Form.Label></Col>
                    <Col><Button variant='outline-danger' disabled={this.props.read} onClick={()=>{this.props.delParam(this.props.keyv)}}>Delete</Button></Col>
                    
                </Row>
            </React.Fragment>
        )
    }
}