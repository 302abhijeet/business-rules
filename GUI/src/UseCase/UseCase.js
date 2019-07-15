import React, { Component } from 'react'
import { Consumer } from '../context';
import {Spinner ,Container,Row,Col,Button} from 'react-bootstrap'
import {Link,Redirect} from 'react-router-dom'
import FormUC from './FormUC'
import SideUC from './SideUC'

export class UseCase extends Component {
    render() {
        return (
            <Consumer>
                {value=>{
                    const {cat} = this.props
                    const {rule,use_cases} = value.value
                    const action =  value.value.actions
                    // if(redirect===true)
                    //     return <Redirect to='/Variable/index' />

                    if(  action===null || action===undefined || rule===null || rule===undefined || use_cases===null || use_cases===undefined){
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
                                        <h1>Usecase</h1>
                                        <p>Click on the Add button to create a usecase or choose a usecase from the given list</p>
                                        <Link to = '/UseCase/add'><Button variant='outline-primary'>Add new usecase</Button></Link>
                                        
                                    </Col>
                                    <Col>
                                        <SideUC use_cases = {use_cases} />
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
                                        <FormUC cat = {cat} readOnly = {readOnly} action={action}  use_cases={use_cases} rule={rule} addData={value.addData} modifyData={value.modifyData} delData={value.delData}/>
                                    </Col>
                                    <Col>
                                        <SideUC use_cases = {use_cases} />
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

export default UseCase
