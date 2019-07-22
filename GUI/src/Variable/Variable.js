import React, { Component } from 'react'
import { Consumer } from '../context';
import {Spinner ,Container,Row,Col,Button} from 'react-bootstrap'
import {Link,Redirect} from 'react-router-dom'
import SideVar from './SideVar'
import FormVar from './FormVar'

export class Variable extends Component {
    render() {
        return (
            <Consumer>
                {value=>{
                    const {cat} = this.props
                    const {variables,in_operation} = value.value
                    const data_sources = value.value.DataSource
                    // if(redirect===true)
                    //     return <Redirect to='/Variable/index' />

                    if( variables === null || variables===undefined || data_sources===null || data_sources===undefined){
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
                                        <SideVar variables = {variables} />
                                    </Col>
                                    <Col lg = {10}>
                                        <h1>Variable</h1>
                                        <p>Click on the Add button to create a variable or choose a variable from the given list</p>
                                        <Link to = '/Variable/add'><Button variant='outline-primary'>Add new Variable</Button></Link>
                                        
                                    </Col>
                                    <Col hidden={!in_operation}>
                                    <Spinner animation="border" role="status">
                                        <span className="sr-only">Loading...</span>

                                    </Spinner>
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
                                        <SideVar variables = {variables} />
                                    </Col>
                                    <Col lg = {10}>
                                        <FormVar cat = {cat} popUp={false} readOnly = {readOnly} data_sources={data_sources} variables={variables} addData={value.addData} modifyData={value.modifyData} delData={value.delData}/>
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

export default Variable
