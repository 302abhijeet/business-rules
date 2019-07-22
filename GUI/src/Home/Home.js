import React, { Component } from 'react'
import { Consumer } from '../context';
import {Accordion,Card, Container, Button,Row,Col,Spinner, ListGroup} from 'react-bootstrap'
import {Link,Redirect} from 'react-router-dom'
import DatePicker from "react-datepicker"
import "react-datepicker/dist/react-datepicker.css";

export class Home extends Component {
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
                        const {use_cases,rules,variables,history} = value.value

                        if( variables === null || variables===undefined || rules===null || rules===undefined || history===null || history===undefined || use_cases===null || use_cases===undefined){
                            return(
                            <Spinner animation="border" role="status">
                                <span className="sr-only">Loading...</span>
                            </Spinner>
                            )
                        }
                        else{
                            return(
                                <Container>
                                    <Row>
                                        <Col><h3>Use Cases</h3></Col>
                                        <Col md="auto"><Link to = {'/UseCase/add'}><Button variant='success' size='md'>ADD</Button></Link></Col>
                                    </Row>
                                    <Accordion>
                                        {use_cases.map(uc => <UCCard name={uc["name"]} rules={uc['rule_list']}/>)}
                                    </Accordion>
                                    <hr/>
                                    <Row>
                                        <Col md="auto"><h3>History: </h3></Col>
                                        <Col md='auto'><h6 style={{marginTop:"10px"}}>FROM:</h6></Col>
                                        <Col md="auto"><DatePicker selected={this.state.start_date} onChange={this.changeStartDate} value={this.state.start_date}/></Col>
                                        <Col md="auto"><h6 style={{marginTop:"10px"}}>TO:</h6></Col>
                                        <Col md="auto"><DatePicker selected={this.state.end_date} onChange={this.changeEndDate} value={this.state.end_date}/></Col>
                                        <Col md='auto'><Button variant="primary" onClick={this.showHistory}>See History</Button></Col>
                                    </Row>
                                    <br />
                                    <Accordion style={{height: '300px',overflowY: 'scroll'}} hidden={!this.state.show_history}>
                                        {history.reverse().filter(ele => new Date(ele["Date"].substr(0,10))<=this.state.end_date && new Date(ele["Date"].substr(0,10))>=this.state.start_date).map(ele => <HistoryCard his={ele} />)}
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
export class HistoryCard extends Component {
    returnFile = (filename) => {
        console.log("http://127.0.0.1:5000/return-files?file=reports\\"+filename.substr(9,))
        fetch("http://127.0.0.1:5000/return-files?file=reports\\"+filename.substr(9,))
            .then(res => res.blob())
            .then(blob => {
                // 2. Create blob link to download
                console.log(blob)
                const url = window.URL.createObjectURL(new Blob([blob]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', filename);
                // 3. Append to html page
                document.body.appendChild(link);
                // 4. Force download
                link.click();
                // 5. Clean up and remove the link
                link.parentNode.removeChild(link);
            })
            .catch(err => {
                console.log(err)
            })
    }
    render(){
        const color = this.props.his["passed"] === undefined?'red':'green'
        return(
            <Card>
                <Accordion.Toggle as={Card.Header} eventKey={this.props.his["Date"]}>
                    <Row>
                        <Col>{this.props.his["Date"]}</Col>
                        <Col sm="auto"><h5 style={{color:color}}>{this.props.his["Use_Case"]}</h5></Col>
                        <Col md="auto"><Button onClick={()=>this.returnFile(this.props.his["Report"])} variant="outline-info">Report</Button></Col>
                    </Row>
                </Accordion.Toggle>
                <Accordion.Collapse eventKey={this.props.his["Date"]}>
                    <Card.Body>
                        <pre>{JSON.stringify(this.props.his,null,'\t')}</pre>
                    </Card.Body>
                </Accordion.Collapse>
            </Card>
        )
    }
}
class UCCard extends Component{
    render(){
        return(
            <Card>
                <Accordion.Toggle as={Card.Header} eventKey={this.props.name}>
                    <Row>
                        {console.log(this.props.name)}
                        {console.log(this.props.rules)}
                        <Col>{this.props.name}</Col>
                        <Col sm="auto"><Link to = {'/History/UseCase/'+this.props.name}><Button variant='outline-warning' size='sm'>History</Button></Link></Col>
                        <Col sm="auto"><Link to = {'/UseCase/'+this.props.name}><Button variant='outline-primary' size='sm'>Modify</Button></Link></Col>
                        <Col sm="auto"><Link to = {'/Run/UseCase/'+this.props.name}><Button variant='outline-info' size="sm">Run</Button></Link></Col>
                    </Row>
                </Accordion.Toggle>
                <Accordion.Collapse eventKey={this.props.name}>
                    <Card.Body>
                        <ListGroup>
                            {this.props.rules.map(ru => <RuleInfo name={ru} />)}
                        </ListGroup>
                    </Card.Body>
                </Accordion.Collapse>
            </Card>
        )
    }
}
class RuleInfo extends Component{
    render(){
        return(
            <ListGroup.Item>
                <Row>
                    <Col>{this.props.name}</Col>
                    <Col sm="auto"><Link to = {'/History/Rule/'+this.props.name}><Button variant='outline-warning' size='sm'>History</Button></Link></Col>
                    <Col sm="auto"><Link to = {'/Rule/'+this.props.name}><Button variant='outline-primary' size='sm'>Modify</Button></Link></Col>
                    <Col sm="auto"><Link to = {`/Run/Rule/${this.props.name}`}><Button variant='outline-info' size="sm">Run</Button></Link></Col>
                </Row>
            </ListGroup.Item>
        )
    }
}

export default Home
