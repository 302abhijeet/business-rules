import React, { Component } from 'react'
import { Form,Row,Col,Button } from 'react-bootstrap';
import Select from 'react-select'
import {Link } from 'react-router-dom'
 import {DisplayActionList} from '../Rule/FormRule'

export class FormUC extends Component {
    
    state={
        name:'',
        rule_list:[],
        rules:[],
        stop_on_first_success:false,
        stop_on_first_failure:false,
        actions_true:[],
        actions_false:[],
        actions:[],
        read:false,
        current_act_true:undefined,
        current_param_true:{},
        current_mt_true:false,
        current_act_false:undefined,
        current_param_false:{},
        current_mt_false:false
    }
    
    componentWillMount = () =>{
        const {cat,use_cases} = this.props
        if(cat!=='add'){
            const uc = use_cases.filter(ele => ele['name']===cat)[0]
            this.setState({...uc,read:true,current_act_true:undefined,
                current_param_true:{},
                current_mt_true:false,
                current_act_false:undefined,
                current_param_false:{},
                current_mt_false:false})
        }
    }
    
    componentWillReceiveProps = nextProps => {
        if(this.props!==nextProps){
            const {cat,use_cases} = nextProps
            if(cat!=='add'){
                const uc = use_cases.filter(ele => ele['name']===cat)[0]
                this.setState({...uc,read:true,current_act_true:undefined,
                    current_param_true:{},
                    current_mt_true:false,
                    current_act_false:undefined,
                    current_param_false:{},
                    current_mt_false:false})
            }else{
                this.setState({
                    name:'',
                    rule_list:[],
                    rules:[],
                    stop_on_first_success:false,
                    stop_on_first_failure:false,
                    actions_true:[],
                    actions_false:[],
                    actions:[],
                    read:false,
                    current_act_true:undefined,
                    current_param_true:{},
                    current_mt_true:false,
                    current_act_false:undefined,
                    current_param_false:{},
                    current_mt_false:false
                })
            }
        }
    }

    changeActs = (values) =>{
        let at = this.state.actions_true, af = this.state.actions_false
        const val = values === null?[]:values.map(ele => ele['label'])
       //filter data
       at = at.filter(ele => val.includes(ele['name']))
       af = af.filter(ele => val.includes(ele['name']))


        this.setState({
            actions: val,
            actions_true:at,
            actions_false:af

        })


      
    }

   

    changeCheck = event => {
        this.setState({[event.target.name]: !this.state[event.target.name]})
    }
    
    onChangeAct = event =>{
        const val = event.target.value
        const params = this.props.actions.filter(
            ele => ele['name'] === val 
        )[0]['params']
        const p={}
        for( let k in params){
            p[k]=''
        }   
        this.setState({
            current_act_true:val,
            current_param_true: p
        })
        this.forceUpdate()
    }

    addTrueAct = () =>{
        const newAct = {}
        newAct['name'] = this.state.current_act_true
        newAct['params']= this.state.current_param_true
        newAct['multi_thread'] = this.state.current_mt_true
        const lst = this.state.actions_true
        lst.push(newAct)
        this.setState({ actions_true:lst })
    }
    
    addActFalse = () =>{
        const newAct = {}
        newAct['name'] = this.state.current_act_false
        newAct['params']= this.state.current_param_false
        newAct['multi_thread'] = this.state.current_mt_false
        const lst = this.state.actions_false
        lst.push(newAct)
        this.setState({ actions_false:lst })
    }

    changeParams = event => {
        const cpt = this.state.current_param_true
        cpt[event.target.name]=event.target.value

        this.setState({ current_param_true:cpt})
    }
    changeParamsFalse = event => {
        const cpt = this.state.current_param_false
        cpt[event.target.name]=event.target.value

        this.setState({ current_param_false:cpt})
    }

    delAction = (listname,keyname) =>{
        console.log(listname)
        console.log(keyname)
        const lst = this.state[listname].filter( ele => ele['name']!==keyname)
        
        this.setState({[listname]:[...lst]})
    }

    onChangeActFalse = event =>{
        const val = event.target.value
        const params = this.props.actions.filter(
            ele => ele['name'] === val 
        )[0]['params']
        const p={}
        for( let k in params){
            p[k]=''
        }   
        this.setState({
            current_act_false:val,
            current_param_false: p
        })
        this.forceUpdate()
    }


    changeCheck = event =>{
        this.setState({[event.target.name]:!this.state[event.target.name]})
    }
    
    modifyRead = () =>{
        this.setState({read:!this.state.read})
    }
    
    
    

    changeState = event =>{
        this.setState({[event.target.name]:event.target.value})
    }
    changeRules = (values) =>{
        
        const val=values === null?[]:values.map(ele => ele['label'])
        this.setState({
            rule_list:val
        })
    }
    
    delData = () =>{

    }

    submitData = () =>{
        
    }
    
    render() {
        const {rules,actions}  = this.props
        const rule_options = rules.map(ele => {
            return {
                'value':ele['name'],
                'label':ele['name']
            }
        })
        const act_options = actions.map(ele => {
            return {
                'value':ele['name'],
                'label':ele['name']
            }
        })
        const cpt = this.state.current_param_true, cpf = this.state.current_param_false
        return (
            <React.Fragment>
                <Form onSubmit = {this.submitData}>
                <Row>
                    <Col>
                    {
                        this.props.cat ==='add' ? <h1>Add new Use Case</h1> : <h1>{this.props.cat} Use Case</h1>
                    } </Col>
                    <Col md='auto'>
                        <Button variant='outline-secondary' onClick={this.modifyRead} disabled={!this.state.read}>Modify</Button>
                    </Col>
                    <Col md='auto'> 
                    <Button variant = 'outline-danger' onClick = {this.delData} disabled = {this.props.cat!=='add'?false:true}>Delete</Button>

                    </Col>
                    </Row>
                    
                    <Form.Group as={Row} controlId='name'>
                        <Form.Label column sm={3}>Name</Form.Label>
                        <Col sm={6}>
                            <Form.Control type='text' name='name' onChange={this.changeState} readOnly={this.props.cat==='add'?false:true} value={this.state.name} />
                        </Col>
                    
                    </Form.Group>

                    <Form.Group as={Row} controlId='rule_list'>
                        <Form.Label column sm={3}>Rules</Form.Label>
                        <Col sm={6}>
                            <Select value={this.state.rule_list.map(ele => {
                                return {
                                    'value':ele,
                                    'label':ele
                                }
                            })} options={rule_options} onChange={this.changeRules} name='rule_list' isMulti isDisabled={this.state.read}/>
                        </Col>
                        <Col>
                        <Link to='/Rule/add'>
                            <Button variant='outline-dark' disabled={this.state.read}  >Add new Rule</Button>
                            </Link>
                        </Col>
                    </Form.Group>


                    <Form.Group as={Row} controlId='actions'>
                        <Form.Label column sm={3}>Actions</Form.Label>
                        <Col sm={6}>
                            <Select value={this.state.actions.map(ele => {
                                return {
                                    'value':ele,
                                    'label':ele
                                }
                            })} options={act_options} onChange={this.changeActs} name='actions' isMulti isDisabled={this.state.read}/>
                        </Col>
                        <Col>
                        <Link to='/Action/add'>
                            <Button variant='outline-dark' disabled={this.state.read}   >Add new Action</Button>
                            </Link>                        
                        </Col>
                    </Form.Group>

                    <Form.Group as = {Row}>
                        <Form.Label column sm={3}>Stop on first success</Form.Label>
                        <Form.Check as ='checkbox' checked={this.state.stop_on_first_success} onChange={this.changeCheck} name='stop_on_first_success' disabled={this.state.read}/>
                    </Form.Group>

                    <Form.Group as = {Row}>
                        <Form.Label column sm={3}>Stop on first failure</Form.Label>
                        <Form.Check as ='checkbox' checked={this.state.stop_on_first_failure} onChange={this.changeCheck} name='stop_on_first_failure' disabled={this.state.read}/>
                    </Form.Group>

                  


                        <hr />

                        <Form.Group as={Row} controlId='actions_trues'>
                        
                        <Form.Label column sm={3}>True actions</Form.Label>
                            
                        <Col sm={4}>
                            <Col>
                            <Form.Control as='select' onChange={this.onChangeAct} value = {this.state.current_act_true} disabled={this.state.read}>
                                <option selected disabled hidden>Select action</option>
                                { this.state.actions.map( ele => <option value={ele}>{ele}</option>     )  }
                            </Form.Control></Col>
                            

                        </Col>
                        <Col sm={4}>
                            <Button variant='outline-danger' onClick={this.addTrueAct} disabled={this.state.read}>Add this action for true</Button>
                        </Col>
                    </Form.Group>


                    {
                                Object.keys(cpt).map( ele =>{
                                    return(
                                        <React.Fragment>
                                                <Form.Group as={Row}>
                                                    <Col sm={3}>
                                                    </Col>
                                                    <Form.Label column sm={3}>{ele}</Form.Label>
                                                    <Col sm={4}>
                                                    <Form.Control type='text' onChange={this.changeParams} name={ele} value={this.state.current_param_true[ele]}/>
                                                    </Col>
                                                    
                                                </Form.Group>

                                        </React.Fragment>
                                    )
                                })
                            }
                            <Form.Group as ={Row}>
                                <Col sm={3}>
                                </Col>
                                <Form.Label column sm={3}>Multithread</Form.Label>
                                <Form.Check as='checkbox' checked={this.state.current_mt_true} onChange={this.changeCheck} name='current_mt_true' disabled={this.state.read}/>

                            </Form.Group>


                        <Row>
                            <Col sm={2}>
                                <strong>List of true actions</strong>
                            </Col>
                            <Col sm={4}>
                                <strong>Parameters</strong>
                            </Col>
                            <Col sm={2}>
                                <strong>Multithreaded</strong>
                            </Col>
                            <Col sm={4}>
                                <strong>Delete</strong>
                            </Col>
                        </Row>
                            
                        {/* displaying action true list*/}
                        {
                            this.state.actions_true.map(ele => <DisplayActionList ele={ele} read={this.state.read} delAction={(keyname)=>this.delAction('actions_true',keyname)}/>)
                        }
                        <hr />
                    
                        {/** Actions False */}
                        <Form.Group as={Row} controlId='actions_false'>
                        
                        <Form.Label column sm={3}>False actions</Form.Label>
                            
                        <Col sm={4}>
                            <Col>
                            <Form.Control as='select' onChange={this.onChangeActFalse} value = {this.state.current_act_false} disabled={this.state.read}>
                                <option selected disabled hidden>Select action</option>
                                { this.state.actions.map( ele => <option value={ele}>{ele}</option>     )  }
                            </Form.Control></Col>
                            

                        </Col>
                        <Col sm={4}>
                            <Button variant='outline-danger' onClick={this.addActFalse} disabled={this.state.read}>Add this action for false</Button>
                        </Col>
                    </Form.Group>


                    {
                                Object.keys(cpf).map( ele =>{
                                    return(
                                        <React.Fragment>
                                                <Form.Group as={Row}>
                                                    <Col sm={3}>
                                                    </Col>
                                                    <Form.Label column sm={3}>{ele}</Form.Label>
                                                    <Col sm={4}>
                                                    <Form.Control type='text' onChange={this.changeParamsFalse} name={ele} value={this.state.current_param_false[ele]}/>
                                                    </Col>
                                                    
                                                </Form.Group>

                                        </React.Fragment>
                                    )
                                })
                            }
                            <Form.Group as ={Row}>
                                <Col sm={3}>
                                </Col>
                                <Form.Label column sm={3}>Multithread</Form.Label>
                                <Form.Check as='checkbox' checked={this.state.current_mt_false} onChange={this.changeCheck} name='current_mt_false' disabled={this.state.read}/>

                            </Form.Group>


                        <Row>
                            <Col sm={2}>
                                <strong>List of False actions</strong>
                            </Col>
                            <Col sm={4}>
                                <strong>Parameters</strong>
                            </Col>
                            <Col sm={2}>
                                <strong>Multithreaded</strong>
                            </Col>
                            <Col sm={4}>
                                <strong>Delete</strong>
                            </Col>
                        </Row>
                            
                        {/* displaying action false list*/}
                        {
                            this.state.actions_false.map(ele => <DisplayActionList ele={ele} read={this.state.read} delAction={(keyname)=>    this.delAction('actions_false',keyname)}/>)
                        }
                        <hr />
                        {/* <Condition2 variables = {this.state.variables} conditions={this.state.conditions} read = {this.state.read} handleConditionChange={this.handleConditionChange}/> */}
                        <hr />

                        <Row>
                            <Col>
                                <Button variant='outline-success' type='submit' disabled={this.state.read}>Submit</Button>
                            </Col>
                            <Col>
                            </Col>
                        </Row>
                

                </Form>



            </React.Fragment>
        )
    }
}

export default FormUC
