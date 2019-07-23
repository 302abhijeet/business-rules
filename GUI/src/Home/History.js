import React, { Component } from 'react'
import { Consumer } from '../context';
import {Accordion,Card, Container, Button,Row,Col,Spinner, ListGroup} from 'react-bootstrap'
import DatePicker from "react-datepicker"
import "react-datepicker/dist/react-datepicker.css"
import {HistoryCard} from "./Home"

export class History extends Component {
    state = {
        start_date:new Date(),
        end_date:new Date(),
        show_history:false
    }
    changeStartDate = (date) => {
        console.log(date)
        this.setState({start_date:date,show_history:false})
    }
    changeEndDate = (date) => {
        this.setState({end_date:date,show_history:false})
    }
    showHistory = () => {
        this.state.start_date.setHours(0)
        this.state.start_date.setMinutes(0)
        this.state.start_date.setSeconds(0)
        this.state.end_date.setHours(23)
        this.state.end_date.setMinutes(59)
        this.state.end_date.setSeconds(59)
        this.setState({show_history:true})
    }
    render() {
        return (
            <React.Fragment>
                <Consumer>
                    {value=>{
                        const {history} = value.value
                        const {type,name} = this.props
                        let passed = 0
                        let failed = 0

                        if( history == null || history == undefined ){
                            return(
                            <Spinner animation="border" role="status">
                                <span className="sr-only">Loading...</span>
                            </Spinner>
                            )
                        }
                        else{
                            if(type === 'UseCase') {
                                history.forEach(ele => {
                                    if(ele["Use_Case"]===name) {
                                        console.log("in history use case")
                                        if(ele["passed"] === undefined) {
                                            console.log("in fail")
                                            ++failed
                                        }
                                        else {
                                            console.log("in pass")
                                            ++passed
                                        }
                                    }
                                })
                            }
                            else {
                                history.forEach(ele => {
                                    if(ele["Rules"] !== undefined && ele["Rules"][name]!==undefined) {
                                        if(ele["Rules"][name]["passed"] === undefined) {
                                            ++failed
                                        }
                                        else {
                                            ++passed
                                        }
                                    }
                                })
                            }
                            return(
                                <Container>
                                    <Row>
                                        <Col><h3>History {type}: {name}</h3></Col>
                                    </Row>
                                    <hr/>
                                    <h5>Total Passed: {passed}</h5>
                                    <h5>Total Failed: {failed}</h5>
                                    <hr />
                                    <Row>
                                        <Col md='auto'><h5>Reports: </h5></Col>
                                        <Col md='auto'><h6>FROM:</h6></Col>
                                        <Col md="auto"><DatePicker selected={this.state.start_date} onChange={this.changeStartDate} value={this.state.start_date}/></Col>
                                        <Col md="auto"><h6>TO:</h6></Col>
                                        <Col md="auto"><DatePicker selected={this.state.end_date} onChange={this.changeEndDate} value={this.state.end_date}/></Col>
                                        <Col md='auto'><Button variant="primary" onClick={this.showHistory}>See History</Button></Col>
                                    </Row>
                                    <br />
                                    <Accordion hidden={!this.state.show_history}>
                                        {   type==="UseCase"? 
                                            history.filter(ele =>ele["Use_Case"]===name && new Date(ele["Date"].substr(0,10))<=this.state.end_date && new Date(ele["Date"].substr(0,10))>=this.state.start_date).map(ele => <HistoryCard his={ele} />)
                                            :history.filter(ele =>ele['Rules']!== undefined  && ele["Rules"][name]!==undefined && new Date(ele["Date"].substr(0,10))<=this.state.end_date && new Date(ele["Date"].substr(0,10))>=this.state.start_date).map(ele => <HistoryCard his={ele} />)
                                        }
                                    </Accordion>
                                </Container>
                            )
                        }
                    }}
                </Consumer>
            </React.Fragment>
        )
    }
}

export default History
