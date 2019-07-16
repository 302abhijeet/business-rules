import React, { Component } from 'react'
import { Consumer } from '../context';
import {Accordion,Card, Container, Button,Row,Col,Spinner, ListGroup} from 'react-bootstrap'
import {Link,Redirect} from 'react-router-dom'

export class Home extends Component {
    render() {
        return (
            <React.Fragment>
                <Consumer>
                    {value=>{
                        const {use_cases,rules,variables} = value.value

                        if( variables === null || variables===undefined || rules===null || rules===undefined || use_cases===null || use_cases===undefined){
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
                                        <Col md="auto"><Link to = {'/UseCase/add'}><Button variant='info' size='md'>ADD</Button></Link></Col>
                                    </Row>
                                    <Accordion>
                                        {use_cases.map(uc => <UCCard name={uc["name"]} rules={uc['rule_list']}/>)}
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
class UCCard extends Component{
    render(){
        return(
            <Card>
                <Accordion.Toggle as={Card.Header} eventKey={this.props.name}>
                    <Row>
                        {console.log(this.props.name)}
                        {console.log(this.props.rules)}
                        <Col>{this.props.name}</Col>
                        <Col sm="auto"><Link to = {'/UseCase/'+this.props.name}><Button variant='outline-secondary' size='sm'>Modify</Button></Link></Col>
                        <Col sm="auto"><Link to = {'/Run/UseCase/'+this.props.name}><Button variant='outline-primary' size="sm">Run</Button></Link></Col>
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
                    <Col sm="auto"><Link to = {'/Rule/'+this.props.name}><Button variant='outline-secondary' size='sm'>Modify</Button></Link></Col>
                    <Col sm="auto"><Link to = {`/Run/Rule/${this.props.name}`}><Button variant='outline-primary' size="sm">Run</Button></Link></Col>
                </Row>
            </ListGroup.Item>
        )
    }
}

export default Home
