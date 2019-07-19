import React, { Component } from 'react'
import { Consumer } from '../context';
import {Spinner ,Container,Row,Col,Button} from 'react-bootstrap'
import {Link,Redirect} from 'react-router-dom'
import SideRule from './SideRule'
import FormRule from './FormRule'

export class Rule extends Component {
    render() {
        return (
            <Consumer>
                {value=>{
                    const {cat} = this.props
                    const {DataSource,actions,rules,variables,redirect} = value.value
                    const action=actions,rule=rules
                    // if(redirect===true)  
                    //     return <Redirect to='/Variable/index' />

                    if( variables === null || variables===undefined || action===null || action===undefined || rule===null || rule===undefined){
                        return(<Spinner animation="border" role="status">
                        <span className="sr-only">Loading...</span>

                      </Spinner>)
                    }else{
                        if(cat === 'index'){
                            return(
                                //Add button here
                                <Container fluid={true}>
                                    <Row>
                                    <Col>
                                        <SideRule rule = {rule} />
                                    </Col>
                                    <Col lg = {10}>
                                        <h1>Rule</h1>
                                        <p>Click on the Add button to create a rule or choose a rule from the given list</p>
                                        <Link to = '/Rule/add'><Button variant='outline-primary'>Add new Rule</Button></Link>
                                        
                                    </Col>
                                    
                                    </Row>
                                </Container>
                            )
                        }else{
                            const readOnly = cat === 'add'? false:true
                            return(
                                <Container fluid={true}>
                                    <Row>
                                    <Col>
                                        <SideRule rule = {rule} />
                                    </Col>
                                    <Col lg = {10}>
                                        <FormRule cat = {cat} readOnly = {readOnly} rule={rule} data_sources={DataSource} actions={action} variables={variables} addData={value.addData} modifyData={value.modifyData} delData={value.delData}/>
                                    </Col>
                                    
                                    </Row>
                                </Container>

                            )
                                                                
                        }
                    }
                }}
            </Consumer>
        )
    }
}

export default Rule
