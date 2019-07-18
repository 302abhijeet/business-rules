import React, { Component } from 'react'
import { Consumer } from '../context';
import {Spinner ,Container,Row,Col,Button} from 'react-bootstrap'
import {Link,Redirect} from 'react-router-dom'
import SideUC from './SideUC'
import FormUC from './FormUC'

export class Rule extends Component {
    render() {
        return (
            <Consumer>
                {value=>{
                    const {cat} = this.props
                    const {actions,rules,use_cases} = value.value
                   
            
                    if( use_cases === null || use_cases===undefined || actions===null || actions===undefined || rules===null || rules===undefined){
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
                                        <SideUC use_cases = {use_cases} />
                                    </Col>
                                    <Col lg = {10}>
                                        <h1>Use Case</h1>
                                        <p>Click on the Add button to create a use case or choose a use case from the given list</p>
                                        <Link to = '/UseCase/add'><Button variant='outline-primary'>Add new Use Case</Button></Link>
                                        
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
                                        <SideUC use_cases = {use_cases} />
                                    </Col>
                                    <Col lg = {10}>
                                        <FormUC cat = {cat} readOnly = {readOnly} rules={rules} actions={actions} use_cases={use_cases} addData={value.addData} modifyData={value.modifyData} delData={value.delData}/>
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
