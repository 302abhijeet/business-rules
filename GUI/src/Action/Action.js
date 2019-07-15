import React, { Component } from 'react'
import { Consumer } from '../context';
import {Spinner ,Container,Row,Col,Button} from 'react-bootstrap'
import {Link,Redirect} from 'react-router-dom'
import SideAct from './SideAct'
import FormAct from './FormAct'



export class Action extends Component {
    render() {
        return (
            <Consumer>
                {value=>{
                    const {cat} = this.props
                    const action = value.value.actions
                    // if(redirect===true)
                    //     return <Redirect to='/Variable/index' />

                    if( action === null || action===undefined){
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
                                        <h1>Action</h1>
                                        <p>Click on the Add button to create an action or choose an action from the given list</p>
                                        <Link to = '/Action/add'><Button variant='outline-primary'>Add new Action</Button></Link>
                                        
                                    </Col>
                                    <Col>
                                        <SideAct actions = {action} />
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
                                        <FormAct cat = {cat} readOnly = {readOnly} actions={action} addData={value.addData} modifyData={value.modifyData} delData={value.delData}/>
                                    </Col>
                                    <Col>
                                        <SideAct actions = {action} />
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

export default Action
