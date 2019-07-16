import React, { Component } from 'react'
import {Consumer} from '../context'
import {Link} from 'react-router-dom'
import {Container,Row,Col,Spinner, Button} from 'react-bootstrap'
import SideDS from './SideDS'
import FormDS from './FormDS'
export class DataSource extends Component {
    
    
    
    render() {

            return (
                <Consumer>
                    {(value) => {
                        const {cat} = this.props
                        const data_sources =value.value.DataSource

                        if( data_sources === null || data_sources===undefined){
                            return(<Spinner animation="border" role="status">
                            <span className="sr-only">Loading...</span>
                          </Spinner>)
                        }                
                        else{
                            if(cat === 'index'){
                                return(
                                    //Add button here
                                    <Container fluid={true}>
                                        <Row>
                                        <Col>
                                            <SideDS data_sources = {data_sources} />
                                        </Col>
                                        <Col lg = {9}>
                                            <h1>Data Source</h1>
                                            <p>Click on the Add button to create a data source or choose a data source from the given list</p>
                                            <Link to = '/DataSource/add'><Button variant='outline-primary'>Add new Data Source</Button></Link>
                                            
                                        </Col>
                                        </Row>
                                    </Container>
                                )
                            }
                            else{
                                const readOnly = cat === 'add'? false:true
                                return(
                                    <Container fluid={true}>
                                        <Row>
                                        <Col>
                                            <SideDS data_sources = {data_sources} />
                                        </Col>
                                        <Col lg = {10}>
                                            <FormDS cat = {cat} readOnly = {readOnly} data_sources={data_sources} addData={value.addData} modifyData = {value.modifyData} delData={value.delData} popUp={false}/>
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

export default DataSource
