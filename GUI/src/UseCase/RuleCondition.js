import React, { Component } from 'react'
import {Form,Row,Col,Button,Dropdown} from 'react-bootstrap'

export class RuleCondition extends Component {
    
    createID = (rootArray,id) =>{
        if(Array.isArray(rootArray)){
            for (let i in rootArray){
                if(typeof rootArray[i] === 'string'){
                    const name = rootArray[i]
                    rootArray[i] = {id,name}
                    id++
                }
                else if(rootArray[i]['all'] || rootArray[i]['any']){
                    rootArray[i]['id'] = id
                    id++
                    if(rootArray[i]['all'])
                        id = this.createID(rootArray[i]['all'],id)
                    else if(rootArray[i]['any'])
                        id = this.createID(rootArray[i]['any'][Object.keys(rootArray[i]['any'])[0]],id)
                    id = this.createID(rootArray[i]['then'],id)
                    id = this.createID(rootArray[i]['else'],id)
                }
                else if(rootArray[i]['multi_thread']){
                    rootArray[i]['id'] =id
                    id++
                    id = this.createID(rootArray[i]['multi_thread'],id)
                }else if(Array.isArray(rootArray[i])){
                    id = this.createID(rootArray[i],id)
                }
            }
        }
        return id

    }



    componentWillMount = () => {
        const {rules} = this.props
        if(rules!==[]){
            const id = this.createID(rules,1)
            this.setState({rules,id})
        }
    }

    componentWillReceiveProps = nextProps => {
        if(nextProps !== this.props){
            const {rules} = nextProps
            if(rules!==[]){
                const id = this.createID(rules,1)
                this.setState({rules,id})
            }else{
                this.setState({rules:[],id:1})
            }
         }
    }

    state = {
        rules:[],
        id:1
    }
    
    addCondition = () =>{
        console.log('add condition')

    }

    convertBack = rule => {
        if(Array.isArray(rule)){
            for(let i in rule){
                if(rule[i]['name']){
                    rule[i] = rule[i]['name']
                }else if(rule[i]['all'] || rule[i]['any']){
                    delete rule[i]['id']
                    if(rule[i]['all'])
                        rule[i]['all'] = this.convertBack(rule[i]['all'])
                    else if(rule[i]['any'])
                        rule[i]['any'] = this.convertBack(rule[i]['any'])
                    rule[i]['then'] = this.convertBack(rule[i]['then'])
                    rule[i]['else'] = this.convertBack(rule[i]['else'])
                }
            }
        }
        return rule
    }

    addRule = () => {
        console.log('add rule')
        console.log(this.state.rules)
    }

    renderrules = () => {
        const {rules} = this.state
        const display = rules.map(ele => {
            if(ele['name']){
                return <RuleVar data={ele} rule_list={this.props.rule_list}/>
            }
            else if(ele['multi_thread']){
                return <Multi data={ele} rule_list={this.props.rule_list} />
            }else if(ele['all'] || ele['any']){
                return <Conditional data={ele} rule_list={this.props.rule_list}/>
            }
        })
        return display
    }
   
    render() {
        return (
            <React.Fragment>
                <Form.Group>
                    <Form.Label column sm ={3}>Rule Condition</Form.Label>
                    <Dropdown>
                        <Dropdown.Toggle variant='outline-secondary' id = 'add'>Add</Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item onClick ={this.addCondition}>Add condition</Dropdown.Item>
                            <Dropdown.Item onClick ={this.addRule}>Add rule</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>

                    {
                        this.renderrules()
                    }
                </Form.Group>
            </React.Fragment>
        )
    }
}

export default RuleCondition


class RuleVar extends Component {




    render() {
        const {data,rule_list} = this.props
        return(
            <React.Fragment>
                {data['id']}
                <Row>
                    <Col sm={6}>
                    <Form.Control as='select' value={data['name'] } >
                        <option hidden value={null}>Select Rule</option>
                        {
                            rule_list.map(ele => <option value={ele}>{ele}</option>)
                        }
                    </Form.Control>
                    </Col>
                    
                    <Col></Col>
                </Row>
            </React.Fragment>
        )
    }
}

class Multi extends Component {



    render() {
        const {data,rule_list} = this.props
        return(
            <React.Fragment>
                <Row>
                {data['id']}
                <Col sm={2}>
                    <Form.Label>Multithreaded</Form.Label>
                </Col>
                <Col sm ={6}>
                    {
                        data['multi_thread'].map(ele => {
                            if(ele['name']){
                                return <RuleVar data={ele} rule_list={this.props.rule_list}/>
                            }
                            else if(ele['multi_thread']){
                                return <Multi data={ele} rule_list={this.props.rule_list} />
                            }else if(ele['all'] || ele['any']){
                                return <Conditional data={ele} rule_list={this.props.rule_list}/>
                            }
                        }) 
                    }
                </Col>
                <Col></Col>
                </Row>
            </React.Fragment>
        )
    }
}

class Conditional extends Component{

    renderData = val => {
        const {data} = this.props
        if(data[val]){
            console.log(data[val])
            if(val==='any'){
                const display = data[val][Object.keys(data['any'])[0]].map(ele => {
                        if(ele['name']){
                            return <RuleVar data={ele} rule_list={this.props.rule_list}/>
                        }
                        else if(ele['multi_thread']){
                            return <Multi data={ele} rule_list={this.props.rule_list} />
                        }else if(ele['all'] || ele['any']){
                            return <Conditional data={ele} rule_list={this.props.rule_list}/>
                        }
                    }
                )
                return display
            }
            else{
            const display = data[val].map(ele => {
                if(ele['name']){
                    return <RuleVar data={ele} rule_list={this.props.rule_list}/>
                }
                else if(ele['multi_thread']){
                    return <Multi data={ele} rule_list={this.props.rule_list} />
                }else if(ele['all'] || ele['any']){
                    return <Conditional data={ele} rule_list={this.props.rule_list}/>
                }
            })
            return display
        }}
    }


    render(){
        const {data} = this.props

        return(
            <React.Fragment>
                <Row>
                    <br />
                    {data['id']}
                    <Col>
                        <Form.Control as='select' value={ data['all']?'all':'any' }>
                            <option value='all'>all</option>
                            <option value='any'>any</option>
                        </Form.Control>
                        {/* {data['any']? data['any'][Object.keys(data['any'])[0]] :''} */}
                        {this.renderData(data['all']?'all':'any')}

                    </Col>
                    <Col>
                        <Form.Label>Then</Form.Label>
                        {this.renderData('then')}
                    </Col>
                    <Col>
                    <Form.Label>else</Form.Label>
                        {this.renderData('else')}
                    </Col>
                </Row><br />
            </React.Fragment>
        )
    }
}












