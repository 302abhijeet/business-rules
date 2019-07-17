import React, { Component } from 'react'
import { Consumer } from '../context';
import {Card, Button,Col, Container,Spinner, ListGroup, Row, Form, ListGroupItem, Accordion } from 'react-bootstrap';
import {Link} from 'react-router-dom'
import FormDS from './../DataSource/FormDS'
import axios from 'axios'

export class Run extends Component {
    state = {
        hideDataSource:true,
        DSList: [],
        DataSource: [],
        name:'',
        isLoading:false,
        parameter_variables :[],
        show_result:true,
        result:{
            run_msg:null,
            data:null,
            file:null,
            parameter_warnings:null
        }
    }
    Vars = []
    showDataSource = () =>{
        if(this.state.name) {
            this.setState({DSList:[...this.state.DSList,this.state.name],hideDataSource:false,name:''})
        }
    }
    changeState = event =>{
        this.setState({[event.target.name]:event.target.value})
    }
    addData = (DS,_id) => {
        console.log("Add data source")
        this.state.DataSource[_id] = DS
    }
    addParameterVariable = (PV) => {
        this.setState({parameter_variables:[...this.state.parameter_variables,PV]})
    }
    delParameterVariable = (PV) => {
        let i=0
        this.state.parameter_variables.forEach(ele => {
            if (ele["name"] === PV["name"]) {
                this.state.parameter_variables.splice(i,1)
            }
            ++i
        })
    }

    runCase = () => {
        this.setState({isLoading:true})
        let url = " http://127.0.0.1:5000/"+ (this.props.type==='UseCase'?"runusecase?use_case=":"runrule?rule=")+ this.props.name
        this.state.parameter_variables.forEach(ele => {
            url += "&"+ele['name']+"="+ele["value"]
        })
        axios.post(url,JSON.stringify(this.state.DataSource))
            .then(res => {
                //console.log(res.data.data)
                this.setState({ result: res.data})
                this.setState({isLoading:false,show_result:false})
            })
            .catch(err => {
                console.log(err)
                this.setState({isLoading:false,show_result:false})
            })
    }
    render() {
        let i=0 
        return (
            <React.Fragment>
                <Consumer>
                    {value=>{
                        const {type,name} = this.props
                        const {use_cases,rules} = value.value

                        if( use_cases === null || rules===null){
                            return(
                                <Spinner animation="border" role="status">
                                    <span className="sr-only">Loading...</span>
                                </Spinner>
                            )
                        }
                        else {
                            if (type === 'UseCase') {
                                console.log(use_cases)
                                const rule_list = use_cases.filter(uc => uc['name'] === name)[0]["rule_list"]
                                console.log(rule_list)
                                let vrs = []
                                rule_list.forEach(ru => {
                                    vrs = [...vrs,...rules.filter(ele => ele["name"]===ru)[0]["variables"]]
                                })
                                this.Vars = [...new Set(vrs)]
                                console.log(this.Vars)
                            }
                            else {
                                let vrs = rules.filter(ele => ele["name"]===name)[0]["variables"]
                                this.Vars = [...new Set(vrs)]
                                console.log(this.Vars)
                            }
                            
                            return(
                                <Container>
                                    <h3>{`Run ${type}: ${name}`}</h3>
                                    <br />
                                    <h5>Variables</h5>
                                    <ListGroup>
                                        {this.Vars.map(vr => <ParameterVariables addParameterVariable={this.addParameterVariable} delParameterVariable={this.delParameterVariable} name={vr}/>)}
                                    </ListGroup>
                                    <br />
                                    <h5>Data Source</h5>
                                    <Row>
                                        <Col md="auto"><Button variant='outline-primary' onClick={this.showDataSource}>Add Data Source</Button></Col>
                                        <Col md="auto"><Form.Control placeholder="Data Source Name" type='text' name='name' onChange={this.changeState} value={this.state.name} /></Col>
                                    </Row>
                                    <br />
                                    <Accordion>
                                        {this.state.DSList.map(uc => <UCCard _id={i++} addData={this.addData} variables={this.Vars} state={uc} name={uc}/>)}
                                    </Accordion>
                                    <br />
                                    <Button variant="outline-success" disabled={this.state.isLoading} onClick={this.runCase}>{this.state.isLoading? 'Loading...': `Run ${type}`}</Button>
                                    <hr />
                                    <div hidden={this.state.show_result}>
                                        <h3>Result</h3>
                                        <Row>
                                            <Col md="auto"><h5>Run Message:</h5></Col>
                                            <Col><h5>{this.state.result["run_msg"]}</h5></Col>
                                        </Row>
                                        {this.state.result["data"]?this.state.result["data"].map(ele => <h6>{JSON.stringify(ele)}</h6>):''}

                                    </div>
                                </Container>
                            )
                        }
                    }}
                </Consumer>
            </React.Fragment>
    
        )
    }
}
class UCCard extends Component{
    render(){
        this.props.addData(null,this.props._id)
        return(
            <Card>
                <Accordion.Toggle as={Card.Header} eventKey={this.props.name}>
                    <Row>
                        <Col>{this.props.name}</Col>
                    </Row>
                </Accordion.Toggle>
                <Accordion.Collapse eventKey={this.props.name}>
                    <Card.Body>
                        <FormDS _id={this.props._id} addData={this.props.addData} variables={this.props.variables} run={true} cat = 'add' readOnly = {false} popUp={false}/>
                    </Card.Body>
                </Accordion.Collapse>
            </Card>
        )
    }
}
class ParameterVariables extends Component {
    state = {
        checked:false,
        value:null
    }
    changeState = event =>{
        let temp = event.target.value
        if(this.state.checked) {
            this.props.delParameterVariable({name:this.props.name,value:this.state.value})
            this.props.addParameterVariable({name:this.props.name,value:temp})
        }
        this.setState({[event.target.name]:event.target.value})
    }
    changeCheck = event =>{
        if(!this.state.checked) {
            console.log("Adding Para checks")
            this.props.addParameterVariable({name:this.props.name,value:this.state.value})
        }
        else {
            console.log("Delete var")
            this.props.delParameterVariable({name:this.props.name,value:this.state.value})
        }
        this.setState({[event.target.name]: !this.state.checked})
    }
    render() {
        return (
            <ListGroup.Item>
                <Row>
                    <Form.Check checked={this.state.checked} type='checkbox'  name='checked' onChange={this.changeCheck} value={this.state.checked} />
                    <Col>{this.props.name}</Col>
                    <Col><Form.Control required={this.state.checked} type='text' name='value' onChange={this.changeState} value={this.state.value} /></Col>
                </Row>
            </ListGroup.Item>
        )
    }
}

export default Run
