import React, { Component } from 'react'
import { isFor } from '@babel/types';
import {Form,Row,Col,Button, ListGroup} from 'react-bootstrap'
import {withRouter} from 'react-router-dom'
export class FormAct extends Component {
    
    state={
        name:'',
        params:{},
        formulae:'',
        read:false,
        key:'',
        value:''
    } 
    
    componentWillMount = () =>{
        const {cat,actions } = this.props
        if(cat!=='add'){
            const data = actions.filter(ele => ele['name']===cat)[0]
            this.setState({...data,read:true,key:'',value:''})
        }else{
            this.setState({
                name:'',
                params:{},
                formulae:'',
                read:false,
                key:'',
                value:''
            })
        }
    }

    componentWillReceiveProps=(nextProps)=>{
        if(nextProps!==this.props){
            const {cat,actions } = nextProps
            if(cat!=='add'){
                const data = actions.filter(ele => ele['name']===cat)[0]
                this.setState({...data,read:true,key:'',value:''})
            }else{
                this.setState({
                    name:'',
                    params:{},
                    formulae:'',
                    read:false,
                    key:'',
                    value:''
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
        this.props.delData('action',this.state['name'])
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
        this.setState({
            params:{...this.state.params,[this.state.key]:this.state.value}
        })
    }

    submitData =() =>{
        console.log('submitting data')
        const data = this.state
        delete data['read']
        delete data['key']
        delete data['value']
        console.log(data)
        if(this.props.cat==='add'){
            console.log('in add')
            this.props.addData('action',data)
            this.props.history.push('/Action/index')

        }else{
            console.log('in '+this.props.cat)
            this.props.modifyData('action',data)
            this.props.history.push('/Action/index')


        }

    }

    render() {
        return (
            <React.Fragment>
                <Form > 
                {
                    this.props.cat ==='add' ? <h1>Add new Action</h1> : <h1>{this.props.cat} Action</h1>
                } 

                <Form.Group as={Row} controlId='name'>
                    <Form.Label column sm={3}>Name</Form.Label>
                    <Col sm={9}>
                        <Form.Control type='text' name='name' onChange={this.changeState} readOnly={this.state.read} value={this.state.name} />
                    </Col>
                
                </Form.Group>
                     
                <Form.Group as={Row} controlId='params'>
                    
                    <Form.Label column sm = {3}>Parameters</Form.Label>
                    <Row>
                        <Col><Form.Control type='text' placeholder='key' name='key' onChange={this.changeState} readOnly={this.state.read} value={this.state.key} /></Col>
                        <Col><Form.Control type='text' placeholder='value' name='value' onChange={this.changeState} readOnly={this.state.read} value={this.state.value} /></Col>
                        <Col><Button variant='outline-secondary' onClick={this.addPara}>Add Parameter</Button></Col>
                    </Row>
                    
                </Form.Group> 
                <Row>
                    <Col>
                    {
                        Object.keys(this.state.params).map(ele => <ParameterDisplay key ={ele} keyv={ele} value={this.state.params[ele]} delParam={this.delParam} read={this.state.read}/>   )
                    }</Col>
                    </Row>

                <Form.Group as={Row} controlId='formulae'>
                    <Form.Label column sm={3}>Formulae</Form.Label>
                    <Col sm={9}>
                        <Form.Control as='textarea' name='formulae' onChange={this.changeState} readOnly={this.state.read} value={this.state.formulae} />
                    </Col>
                </Form.Group>

                </Form>
                <Row>
                        <Col><Button type = 'submit' variant='outline-success' disabled={this.state.read} onClick={this.submitData}>Submit</Button></Col>
                        <Col><Button name='modify' variant='outline-secondary' disabled={!this.state.read} onClick={this.changeReadMode}>Modify</Button></Col>
                        <Col><Button name = 'delete' variant='outline-danger' disabled={this.state.read} onClick={this.deleteData}>Delete</Button></Col>
                    </Row>

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