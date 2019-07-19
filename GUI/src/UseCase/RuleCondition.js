import React, { Component } from 'react'
import {Form,Row,Col,Button,Dropdown, ListGroup} from 'react-bootstrap'

export class RuleCondition extends Component {
    
    createID = (rootArray,id) =>{
        if(Array.isArray(rootArray)){
            if(!Number.isInteger(rootArray[0]) || rootArray[0]!==undefined || rootArray[0]!==null){
                console.log(rootArray[0])
                rootArray.unshift(id)
            }
            id++



            for (let i in rootArray){
                if(Number.isInteger(rootArray[i]))
                    continue

                else if(typeof rootArray[i] === 'string'){
                    const name = rootArray[i]
                    rootArray[i] = {id,name}
                    id++
                }
                else if(typeof rootArray[i]==='object' && ('all' in rootArray[i]|| 'any' in rootArray[i])){
                    rootArray[i]['id'] = id
                    id++
                    if(rootArray[i]['all'])
                        id = this.createID(rootArray[i]['all'],id)
                    else if(rootArray[i]['any'])
                        id = this.createID(rootArray[i]['any'][Object.keys(rootArray[i]['any'])[0]],id)
                    if(rootArray[i]['then'])
                        id = this.createID(rootArray[i]['then'],id)
                    if(rootArray[i]['else'])    
                        id = this.createID(rootArray[i]['else'],id)
                }
                else if(typeof rootArray[i]==='object' && 'multi_thread' in rootArray[i]){
                    rootArray[i]['id'] =id
                    id++
                    id = this.createID(rootArray[i]['multi_thread'],id)
                }else if(Array.isArray(rootArray[i])){
                    id = this.createID(rootArray[i],id)
                }
            }
            return id
        }
        

    }



    componentWillMount = () => {
        const {rules} = this.props
        if(rules.length!==0){
            const id = this.createID(rules,1)
            this.setState({rules,id})
        }
    }

    componentWillReceiveProps = nextProps => {
        if(nextProps !== this.props){
            const {rules} = nextProps
            if(rules.length!==0){
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

    getID = (id,data) =>{
        let stack = []
        stack.push(data)
        while(stack.length!==0){
            const element = stack.pop()  
            if(Number.isInteger(element) || element===null)
                continue        
            if(Array.isArray(element)){
                if(element[0]===id)
                    return element
                else    
                    stack = [...stack,...element]
            }
            else if(typeof element === 'object' && 'name' in element){
                if(element['id'] === id){
                    return element
                }
            }
            else if(typeof element === 'object' &&'multi_thread' in element){
                if(element['id'===id]){
                    return element
                }
                else{
                    stack = [...stack,element['multi_thread']]
                }
            }
            else if(typeof element === 'object' && ('all' in element|| 'any'in element)){
                if(element['id']===id){
                    return element
                }
                else{
                    if('all' in element)
                        stack = [...stack,element['all']]
                    else if('any' in element)
                        stack = [...stack,element['any'][Object.keys(element['any'])[0]]]

                    if('then' in element)
                        stack = [...stack,element['then']]

                    if('else' in element)
                        stack = [...stack,element['else']]
                }
            }

        }
        return false


    } 


    //Data addition functions
    addRule = (obid) => {
        const {rules} = this.state
        const ob = this.getID(obid,rules)
        console.log(ob)
        ob.push({ name:'',id:this.state.id +1  })
        this.props.handleRulesChange(rules,this.state.id+1)
        //this.setState({rules,id:this.state.id+1})
    }

    modCondition = (id,newval) =>{
        const {rules} = this.state
        const ob = this.getID(id,rules)
        if(typeof ob === 'object' && 'all' in ob){
            ob[newval] = {1:ob['all']}
            delete ob['all']

        }else if(typeof ob ==='object' && 'any' in ob){
            ob[newval] = ob['any'][Object.keys(ob['any'])[0]]
            delete ob['any']
        }
        this.props.handleRulesChange(rules,this.state.id)
//        this.setState({rules})
    }

    modAny = (id,newval) => {
        const {rules} = this.state
        const ob = this.getID(id,rules)
        if(typeof ob==='object' && 'any' in ob){
            console.log(newval)
            const delkey = Object.keys(ob['any'])[0]
            console.log(delkey)
            ob['any'][newval] = ob['any'][delkey]
            delete ob['any'][delkey]
            console.log(ob)

        }
        this.props.handleRulesChange(rules,this.state.id)
        // this.setState({rules})
    }

    addCondition = (obid) =>{
        
        const {rules,id} = this.state
        const ob = this.getID(obid,rules)
        ob.push({'all':[id+1],'then':[id+2],'else':[id+3],id:this.state.id+4})
        this.props.handleRulesChange(rules,this.state.id+4)
        // this.setState({rules,id:this.state.id+4})
    }

    addMulti = (obid) => {
        const {rules,id} = this.state
        const ob = this.getID(obid,rules)
        ob.push({'multi_thread':[id+1],id:id+2})
        this.props.handleRulesChange(rules,this.state.id+2)
        // this.setState({rules,id:id+2})
    }

    modRule = (id,newval) =>{
        console.log('mod rule')
        const {rules} = this.state
        const ob = this.getID(id,rules)
        ob['name'] = newval
        this.props.handleRulesChange(rules,this.state.id)
        // this.setState({rules})
    }

  

    //Data deletion functions
    delData = (id,parentId) =>{
        console.log('del rule')
        const {rules} = this.state
        //const ob = this.getID(id,rules)
        let pob
        if(parentId!==null)
             pob = this.getID(parentId,rules)
        else    
            pob = rules
        let ind
        if(Array.isArray(pob)){

            for(let i in pob){
                if(Number.isInteger(pob[i]))    
                    continue
                if(typeof pob[i] === 'object' && 'id' in pob[i]){
                    if(pob[i]['id']===id){
                        ind = i
                        break
                    }
                }
            }
            pob.splice(ind,1)
        }
        console.log(pob)
        this.props.handleRulesChange(rules,this.state.id)
        // this.setState({rules})

    }



   
    render() {
        return (
            <React.Fragment>
                <Form.Group>
                    <Form.Label column sm ={3}>Rule Condition</Form.Label>
                    
                    
                    <ListGroup>
                    {
                        <RuleArr data={this.state.rules} rule_list={this.props.rule_list} modRule={this.modRule} delData={this.delData} parentId={null} addCondition={this.addCondition} addMulti={this.addMulti} addRule={this.addRule} modAny= {this.modAny} modCondition={this.modCondition}  />
                    }
                    </ListGroup>
                    
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
                <ListGroup.Item>
                <Row>
                    <Col sm={6}>
                    
                    <Form.Control as='select' value={data['name'] } onChange={event=>this.props.modRule(data['id'],event.target.value)} >
                        <option hidden value="">Select Rule</option>
                        {
                            rule_list.map(ele => <option value={ele}>{ele}</option>)
                        }
                    </Form.Control>
                    </Col>
                    <Col>
                        <Button variant='outline-danger' onClick={()=>this.props.delData(data['id'],this.props.parentId)} >Delete</Button>
                    </Col>
                    </Row></ListGroup.Item>
            </React.Fragment>
        )
    }
}

class Multi extends Component {



    render() {
        const {data,rule_list,modRule,delData,addCondition,addMulti,addRule,modCondition,modAny} = this.props
        return(
            <React.Fragment>
                <ListGroup.Item>
                <Row>
                <Col sm={2}>
                    <Form.Label>Multithreaded</Form.Label>
                </Col>
                <Col sm ={6}>
                    <RuleArr data={data['multi_thread'] } rule_list={rule_list} modRule={modRule} delData={delData}  parentId={data['id']}  addCondition={addCondition} addMulti={addMulti} addRule={addRule} modCondition={modCondition} modAny={modAny}/>
                </Col>
                <Col>
                    <Button variant='outline-danger' onClick={()=>this.props.delData(data['id'],this.props.parentId)} >Delete</Button>
                </Col>
                </Row></ListGroup.Item>
            </React.Fragment>
        )
    }
}

class Conditional extends Component{

    renderData = val => {
        const {data,rule_list,modRule,delData,addCondition,addMulti,addRule,modCondition,modAny} = this.props
        if(data[val]){
            if(val==='any'){
              
                return <RuleArr data={data[val][Object.keys(data['any'])[0]]} rule_list = {rule_list} modRule={modRule} delData={delData} parentId={data['id']}  addCondition={addCondition} addMulti={addMulti} addRule={addRule} modCondition={modCondition} modAny={modAny}/>
            }
            else{
                return <RuleArr data={data[val]} rule_list={rule_list} modRule={modRule} delData={delData}  parentId={data['id']}  addCondition={addCondition} addMulti={addMulti} addRule={addRule} modCondition={modCondition} modAny={modAny}/>
            }
        }
    }


    render(){
        const {data} = this.props

        return(
            <React.Fragment>
                <ListGroup.Item>
                <Row>
                    <br />
                    <ListGroup.Item>
                    <Col>
                        <Form.Control as='select' value={ 'all' in data?'all':'any' } onChange={e => this.props.modCondition(data['id'],e.target.value)}>
                            <option value='all'>all</option>
                            <option value='any'>any</option>
                        </Form.Control>
                        <Col hidden={'any' in data?false:true}>
                            <Form.Control type = 'text' value={ 'any' in data ? Object.keys(data['any'])[0]:'' } onChange={event=>this.props.modAny(data['id'],event.target.value)}/>
                        </Col>
                            {/* {data['any']? data['any'][Object.keys(data['any'])[0]] :''} */}
                        {this.renderData(data['all']?'all':'any')}

                    </Col>
                    
                    </ListGroup.Item>
                    <ListGroup.Item>
                    <Col>
                        <Form.Label>Then</Form.Label>
                        {this.renderData('then')}
                    </Col></ListGroup.Item>
                    <ListGroup.Item>
                    <Col>
                    <Form.Label>else</Form.Label>
                        {this.renderData('else')}
                    </Col>
                    </ListGroup.Item>
                    <ListGroup.Item>
                    <Col><Button variant='outline-danger' onClick={()=>this.props.delData(data['id'],this.props.parentId)}>Delete </Button></Col>

                    </ListGroup.Item>
                </Row></ListGroup.Item><br />
            </React.Fragment>
        )
    }
}

class RuleArr extends Component{


    renderRules = (data) =>{
        const {rule_list,modRule,delData,addCondition,addMulti,addRule,modCondition,modAny} = this.props
        const display = data.map(ele => {
            if(Number.isInteger(ele)){}
                
            else if(typeof ele === 'object' && 'name' in ele){
                return <RuleVar data={ele} rule_list={rule_list} modRule={modRule} delData={delData} parentId={data[0]} modCondition={modCondition} modAny={modAny}/>
            }
            else if(typeof ele === 'object' && 'multi_thread' in ele){
                return <Multi data={ele} rule_list={rule_list} modRule={modRule} delData={delData} parentId={data[0]} addCondition={addCondition} addMulti={addMulti} addRule={addRule} modCondition={modCondition} modAny={modAny}/>
            }else if(typeof ele === 'object' && ('all' in ele || 'any' in ele)){
                return <Conditional data={ele} rule_list={rule_list} modRule={modRule} delData={delData} parentId={data[0]}  addCondition={addCondition} addMulti={addMulti} addRule={addRule} modCondition={modCondition} modAny={modAny}/>
            }else if(Array.isArray(ele)){
                //array in array, pass the state as a parameter and make this function recursive
                return this.renderRules(ele)
            }
        })
        return display
    }

    render(){
        return(
            <React.Fragment>
            <ListGroup.Item>
                    <Dropdown>
                        <Dropdown.Toggle variant='outline-secondary' id = 'add'>Add</Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item onClick ={()=>this.props.addCondition(this.props.data[0])}>Add condition</Dropdown.Item>
                            <Dropdown.Item onClick ={()=>this.props.addRule(this.props.data[0])}>Add rule</Dropdown.Item>
                            <Dropdown.Item onClick = {()=>this.props.addMulti(this.props.data[0])}>Add multithread</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                    {
                        this.renderRules(this.props.data)
                    }
                </ListGroup.Item>
            </React.Fragment>
        )
    }

}










