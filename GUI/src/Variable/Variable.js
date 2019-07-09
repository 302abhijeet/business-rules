import React, { Component } from 'react'
import { Consumer } from '../context';
import {Spinner ,Container,Row,Col,Button} from 'react-bootstrap'
import {Link} from 'react-router-dom'
import SideVar from './SideVar'
import FormVar from './FormVar'

export class Variable extends Component {
    render() {
        return (
            <Consumer>
                {value=>{
                    const {cat} = this.props
                    const {data_sources,variables} = value.value
                    if( variables === null || variables===undefined){
                        return(<Spinner animation="border" role="status">
                        <span className="sr-only">Loading...</span>

                      </Spinner>)
                    }else{
                        if(cat === 'index'){
                            return(
                                //Add button here
                                <Container>
                                    <Row>
                                    <Col lg = {9}>
                                        <h1>Variable</h1>
                                        <p>Click on the Add button to create a variable or choose a variable from the given list</p>
                                        <Link to = '/Variable/add'><Button variant='outline-primary'>Add new Variable</Button></Link>
                                        
                                    </Col>
                                    <Col>
                                        <SideVar variables = {variables} />
                                    </Col>
                                    </Row>
                                </Container>
                            )
                        }else{
                            const readOnly = cat === 'add'? false:true
                            return(
                                <Container>
                                    <Row>
                                    <Col lg = {9}>
                                        <FormVar cat = {cat} readOnly = {readOnly} data_sources={data_sources} variables={variables} />
                                    </Col>
                                    <Col>
                                        <SideVar variables = {variables} />
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
