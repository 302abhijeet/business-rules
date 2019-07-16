import React, { Component } from 'react'
import Iframe from 'iframe-react'
import {Modal,Form,Row,Col, Button} from 'react-bootstrap'
import {Link,withRouter} from 'react-router-dom'
import FormDS from './../DataSource/FormDS'

export class FormVar extends Component {
    
    state = {
        name:'',
        field:'',
        label:'None',
        options:'None',
        formulae:'',
        input_method:{
            DataSource:'',
            command:'',
            evaluation:'',
            start:null,
            end:null
        },
        multi_thread:true,
        cashe:true,
        derived:true,
        validated:false,
        read:false,
        show_modal:false,
        show_dataSource:false
    }
    
    componentWillMount = () =>{
        const {cat,variables} = this.props
        
        if(cat!=='add'){
            variables.forEach(element => {
                if(element['name'] === cat){
                    this.setState({...element,derived:element['input_method']['DataSource']?false:true,read:true,validated:false,show_modal:false})
                }
            })
                
        
        }else{
            this.setState({
                name:'',
                field:'',
                label:'None',
                options:'None',
                formulae:'',
                input_method:{
                    DataSource:'',
                    command:'',
                    evaluation:'',
                    start:null,
                    end:null
                },
                multi_thread:true,
                cashe:true,
                derived:true,
                validated:false,
                read:false,
                show_modal:false
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
                        this.setState({...element,derived:element['input_method']['DataSource']?false:true,read:true,validated:false})
                    }
                })
                    
            
            }else{
                this.setState({
                    name:'',
                    field:'',
                    label:'None',
                    options:'None',
                    formulae:'',
                    input_method:{
                        DataSource:'',
                        command:'',
                        evaluation:'',
                        start:null,
                        end:null
                    },
                    multi_thread:true,
                    cashe:true,
                    derived:true,
                    validated:false,
                    read:false,
                    show_modal:false
                })
            }
        }
    }
    deleteData = () =>{
        //delete data from context
        this.props.delData('variables',{name:this.state['name']})
        //Redirect?
        this.props.history.push('/Variable/index')
    }

    changeState = event =>{
        if(event.target.name==='name') {
            this.setState({formulae:"self.product."+event.target.value})
        }
        this.setState({
            [event.target.name]:event.target.value
        })
    }
    changeStatedb =event =>{
        if (event.target.value === 'derived') {
            this.setState({derived:true} )
        }
        else {
            this.setState({derived:false})
        }
        this.changeStateim(event)
    }
    changeStateim =event =>{
        const im = this.state.input_method
        im[event.target.name] = event.target.value
        this.setState({input_method:im})
    }
    changeCheck = event =>{
        this.setState({[event.target.name]: !this.state.multi_thread})
    }
    changeCheckCache = event =>{
        this.setState({[event.target.name]: !this.state.cashe})
    }
    changeReadMode = () =>{
        this.setState({
            read:!this.state.read
        })
    }
    closeModal = () => {
        this.setState({show_modal:false})
    }
    showModal = () => {
        this.setState({show_modal:true})
    }
    closeDataSourceModal = () => {
        this.setState({show_dataSource:false})
    }
    showDataSourceModal = () => {
        this.setState({show_dataSource:true})
    }
    submitForm=(e)=>{
        const form = e.currentTarget
        if (form.checkValidity() === false) {
            e.preventDefault()
            e.stopPropagation()
        }
        else {
            e.preventDefault() 
            let data = this.state
            delete data["read"]
            delete data["derived"]
            delete data["validated"]
            delete data["show_modal"]
            if (data["input_method"]["DataSource"] === "derived"){
                delete data["input_method"]["DataSource"]
                delete data["input_method"]["command"]
                delete data["input_method"]["evaluation"]
                delete data["input_method"]["start"]
                delete data["input_method"]["end"]
                data["input_method"]["method"] = "derived"
            }
            else {
                try {
                    delete data["input_method"]["method"]
                    data["input_method"]["start"] = data["input_method"]["start"]?data["input_method"]["start"]:null
                    data["input_method"]["end"] = data["input_method"]["end"]?data["input_method"]["end"]:null
                }
                catch {}
            }
            if(this.props.cat === 'add'){
                if( this.props.variables.filter( ele => ele['name']===data['name']).length > 0){
                    e.stopPropagation()
                    this.showModal()
                    return false
                }
                this.props.addData('variables',data)
            }
            else{
                let newData = {
                    querry : {name : data["name"]},
                    newData : data
                } 
                this.props.modifyData('variables',newData)
            }
            this.props.history.push('/Variable/index')
        }
        this.setState({validated:true})
        

    }
    
    render() {


        const {data_sources} = this.props
        const list_of_ds = data_sources.map(ele => ele['name'])
        const {validated} = this.state
        
        return (
            <React.Fragment>
            <Modal show={this.state.show_modal}>
                <Modal.Header closeButton><Modal.Title>Cannot ADD variable</Modal.Title></Modal.Header>
                <Modal.Body> <p>Variable name already exists!</p></Modal.Body>
                <Modal.Footer><Button variant="secondary" onClick={this.closeModal}>Close</Button></Modal.Footer>
            </Modal>
            <Modal size='xl' scrollable size="Large"  scrollable show={this.state.show_dataSource}>
                <Modal.Header closeButton><Modal.Title>ADD Data Source</Modal.Title></Modal.Header>
                <Modal.Body> 
                    <FormDS cat = 'add' readOnly = {false} data_sources={data_sources} addData={this.props.addData} popUp={true} closeDataSourceModal={this.closeDataSourceModal}/>
                </Modal.Body>
                <Modal.Footer><Button variant="secondary" onClick={this.closeDataSourceModal}>Close</Button></Modal.Footer>
            </Modal>
            <Form noValidate validated={validated} onSubmit={this.submitForm}>
                {
                    this.props.cat ==='add' ? <h1>Add new Variable</h1> : <h1>{this.props.cat} Variable</h1>
                }   
                
                    <Form.Group as={Row} controlId='name'>
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Name</Form.Label>
                        <Col sm={9}>
                            <Form.Control required type='text' name='name' onChange={this.changeState} readOnly={this.state.read} value={this.state.name} />
                            <Form.Control.Feedback type="invalid">Enter Variable Name!</Form.Control.Feedback>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='field'>
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Field</Form.Label>
                        <Col sm={9}>
                            <Form.Control required as='select' name='field' onChange={this.changeState} disabled={this.state.read} value={this.state.field}>
                                    <option value="" selected hidden>
                                        Select an option
                                    </option>
                                    <option value = 'numeric_rule_variable'>
                                        numeric
                                    </option>
                                    <option value = 'string_rule_variable'>
                                        string
                                    </option>
                                    <option value = 'boolean_rule_variable'>
                                        boolean
                                    </option>
                                    <option value = 'select_rule_variable'>
                                        select
                                    </option>
                                    <option value = 'select_multiple_rule_variable'>
                                        select_multiple
                                    </option>
                            </Form.Control>
                            <Form.Control.Feedback type="invalid">Enter type of variable!</Form.Control.Feedback>
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

                    <Form.Group as={Row} controlId='DataSource'>
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Data Source</Form.Label>
                        <Col sm={6}>
                            <Form.Control required as='select' name='DataSource' onChange={this.changeStatedb} disabled={this.state.read} value={this.state.input_method.DataSource}>
                                {list_of_ds.map(ele => <option value={ele}>{ele}</option>)}
                                <option value = 'derived'>
                                        None
                                </option>
                                <option value="" selected hidden>
                                        Select an option
                                </option>
                            </Form.Control>
                            <Form.Control.Feedback type="invalid">Please select None if variable is "derived"</Form.Control.Feedback>
                        </Col>
                        <Col>
                            <Button variant='outline-secondary' onClick={this.showDataSourceModal} disabled={this.state.read}>Add new Data Source</Button>
                        </Col>
                    </Form.Group>
            


                    <Form.Group as={Row} controlId='formulae' hidden={!this.state.derived}>
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Formulae</Form.Label>
                        <Col sm={9}>
                            <Form.Control required type='text' name='formulae' onChange={this.changeState} readOnly={this.state.read} value={this.state.formulae} />
                            <Form.Control.Feedback type="invalid">Enter formulae if vaiable is derived</Form.Control.Feedback>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='command' hidden={this.state.derived}>
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Command</Form.Label>
                        <Col sm={9}>
                            <Form.Control required={!this.state.derived} type='text' name='command' onChange={this.changeStateim} readOnly={this.state.read} value={this.state.input_method.command} />
                            <Form.Control.Feedback type="invalid">Enter command if vaiable is to be fetched</Form.Control.Feedback>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='evaluation' hidden={this.state.derived}>
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Evaluation</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' required={!this.state.derived} name='evaluation' onChange={this.changeStateim} readOnly={this.state.read} value={this.state.input_method.evaluation} />
                            <Form.Control.Feedback type="invalid">Enter type of variabe for evaluation(int,string)</Form.Control.Feedback>
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='start' hidden={this.state.derived}>
                        <Form.Label column sm={3}>Start</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' defaultValue={null} name='start' onChange={this.changeStateim} readOnly={this.state.read} value={this.state.input_method.start} />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row}controlId='end' hidden = {this.state.derived}>
                        <Form.Label column sm={3}>End</Form.Label>
                        <Col sm={9}>
                            <Form.Control type='text' defaultValue={null} name='end' onChange={this.changeStateim} readOnly={this.state.read} value={this.state.input_method.end} />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='cache'>
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Cache</Form.Label>
                        <Col sm={9}>
                            <Form.Check checked={this.state.cashe} type='checkbox' name='cache' onChange={this.changeCheckCache} readOnly={this.state.read} value={this.state.cashe} />
                        </Col>
                    </Form.Group>

                    <Form.Group as={Row} controlId='multi_thread'>
                        <Form.Label column sm={3}><span style={{color:"red"}}>*</span>Multi-thread</Form.Label>
                        <Col sm={9}>
                            <Form.Check checked={this.state.multi_thread} required type='checkbox'  name='multi_thread' onChange={this.changeCheck} readOnly={this.state.read} value={this.state.multi_thread} />
                        </Col>
                    </Form.Group>

                    <Row>
                        <Col><Button type = 'submit' variant='outline-success' disabled={this.state.read}>Submit</Button></Col>
                        <Col><Button name='modify' variant='outline-secondary' disabled={!this.state.read} onClick={this.changeReadMode}>Modify</Button></Col>
                        <Col><Button name = 'delete' variant='outline-danger' disabled={!this.state.read} onClick={this.deleteData}>Delete</Button></Col>
                    </Row>

            </Form>                

            </React.Fragment>

        )
    }
}

export default withRouter(FormVar)
    
