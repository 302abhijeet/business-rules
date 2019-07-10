import React, { Component } from 'react'
import {Form,Row,Col, Button} from 'react-bootstrap'
import {Link,withRouter} from 'react-router-dom'


export class FormVar extends Component {
    
    state = {
        name:'',
        field:'',
        label:'',
        options:'',
        formulae:'',
        input_method:{
            DataSource:'',
            command:'',
            evaluation:'',
            start:'',
            end:''
        },
        read:false
    }
    
    componentWillMount = () =>{
        const {cat,variables} = this.props
        
        if(cat!=='add'){
            variables.forEach(element => {
                if(element['name'] === cat){
                    this.setState({...element,read:true})
                }
            })
                
        
        }else{
            this.setState({
                name:'',
                field:'',
                label:'',
                options:'',
                formulae:'',
                input_method:{
                    DataSource:'',
                    command:'',
                    evaluation:'',
                    start:'',
                    end:''
                },
                read:false
            })
        }
    }

    componentWillReceiveProps = (nextProps)=>{
        if(nextProps!== this.props){
            const {cat,variables} = nextProps
            if(cat!=='add'){
                variables.forEach(element => {
                    if(element['name'] === cat){
                        if(element['input_method']['start']===null)
                            element['input_method']['start']=''
                            if(element['input_method']['end']===null)
                            element['input_method']['end']=''
                        this.setState({...element,read:true})
                    }
                })
                    
            
            }else{
                this.setState({
                    name:'',
                    field:'',
                    label:'',
                    options:'',
                    formulae:'',
                    input_method:{
                        DataSource:'',
                        command:'',
                        evaluation:'',
                        start:'',
                        end:''
                    },
                    read:false
                })
            }
        }
    }
    deleteData = () =>{
        //delete data from context
        this.props.delData('variables',this.state['name'])
        //Redirect?
        this.props.history.push('/Variable/index')
    }

    changeState = event =>{
        this.setState({
            [event.target.name]:event.target.value
        })
    }
    changeStateim =event =>{
        const im = this.state.input_method
        im[event.target.name] = event.target.value
        this.setState({input_method:im})
    }
    changeReadMode = () =>{
        this.setState({
            read:!this.state.read
        })
    }

    submitForm=(e)=>{
        e.preventDefault()
        if(this.props.cat === 'add'){
            
            this.props.addData('variables',this.state)

        }else{
            this.props.modifyData('variables',this.state)
        }
    }
    
    render() {


        const {data_sources} = this.props
        const list_of_ds = data_sources.map(ele => ele['name'])
        
        return (
            <React.Fragment>
            <Form onSubmit={this.submitForm}>
                {
                    this.props.cat ==='add' ? <h1>Add new Variable</h1> : <h1>{this.props.cat} Variable</h1>
                }   
                
                <Form.Group as={Row} controlId='name'>
                        <Form.Label column sm={3}>Name</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='name' onChange={this.changeState} readOnly={this.state.read} value={this.state.name} />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='field'>
                        <Form.Label column sm={3}>Field</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='field' onChange={this.changeState} readOnly={this.state.read} value={this.state.field} />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='label'>
                        <Form.Label column sm={3}>Label</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='label' onChange={this.changeState} readOnly={this.state.read} value={this.state.label} />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='options'>
                        <Form.Label column sm={3}>Option</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='options' onChange={this.changeState} readOnly={this.state.read} value={this.state.options} />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='formulae'>
                        <Form.Label column sm={3}>Formulae</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='formulae' onChange={this.changeState} readOnly={this.state.read} value={this.state.formulae} />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='DataSource'>
                        <Form.Label column sm={3}>Data Source</Form.Label>
                        <Col sm={6}>
                            <Form.Control as='select' name='DataSource' onChange={this.changeStateim} disabled={this.state.read} value={this.state.input_method.DataSource}>
                                
                                {list_of_ds.map(ele => <option value={ele}>{ele}</option>)}

                            </Form.Control>
                        </Col>
                        <Col>
                            <Link to='/DataSource/add'><Button variant='outline-secondary' disabled={this.state.read}>Add new Data Source</Button></Link>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='command'>
                        <Form.Label column sm={3}>Command</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='command' onChange={this.changeStateim} readOnly={this.state.read} value={this.state.input_method.command} />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='evaluation'>
                        <Form.Label column sm={3}>Evaluation</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='evaluation' onChange={this.changeStateim} readOnly={this.state.read} value={this.state.input_method.evaluation} />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='start'>
                        <Form.Label column sm={3}>Start</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='start' onChange={this.changeStateim} readOnly={this.state.read} value={this.state.input_method.start} />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='end'>
                        <Form.Label column sm={3}>End</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' name='end' onChange={this.changeStateim} readOnly={this.state.read} value={this.state.input_method.end} />
                        </Col>
                    </Form.Group>
                    <Row>
                        <Col><Button type = 'submit' variant='outline-success' disabled={this.state.read}>Submit</Button></Col>
                        <Col><Button name='modify' variant='outline-secondary' disabled={!this.state.read} onClick={this.changeReadMode}>Modify</Button></Col>
                        <Col><Button name = 'delete' variant='outline-danger' disabled={this.state.read} onClick={this.deleteData}>Delete</Button></Col>
                    </Row>

            </Form>                

            </React.Fragment>

        )
    }
}

export default withRouter(FormVar)
    
