import React, { Component } from 'react'
import {Form,Row,Col,Button,Dropdown, ListGroup} from 'react-bootstrap'

export class RuleCondition extends Component {
    createID = (rootArray,count) =>{
        if(Array.isArray(rootArray)){
            if(!Number.isInteger(rootArray[0]) && rootArray[0]!==undefined && rootArray[0]!==null){
                rootArray.unshift(count)
            }
            count++



            for (let i in rootArray){
                if(Number.isInteger(rootArray[i]))
                    continue

                else if(typeof rootArray[i] === 'string'){
                    const name = rootArray[i]
                    rootArray[i] = {id:count,name}
                    count++
                }
                else if(typeof rootArray[i]==='object' && ('all' in rootArray[i]|| 'any' in rootArray[i])){
                    rootArray[i]['id'] = count
                    count++
                    if(rootArray[i]['all'])
                        count = this.createID(rootArray[i]['all'],count)
                    else if(rootArray[i]['any'])
                        count = this.createID(rootArray[i]['any'][Object.keys(rootArray[i]['any'])[0]],count)
                    if(rootArray[i]['then'])
                        count = this.createID(rootArray[i]['then'],count)
                    if(rootArray[i]['else'])    
                        count = this.createID(rootArray[i]['else'],count)
                }
                else if(typeof rootArray[i]==='object' && 'multi_thread' in rootArray[i]){
                    rootArray[i]['id'] =count
                    count++
                    count = this.createID(rootArray[i]['multi_thread'],count)
                }else if(Array.isArray(rootArray[i])){
                    count = this.createID(rootArray[i],count)

                }
            }
        }
        return count
        

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
                this.setState({rules,id:this.props.count})
            }else{
                this.setState({rules:[],id:1})
            }
         }
    }

    state = {
        rules:[],

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
        const {count} = this.props
        const ob = this.getID(obid,rules)
        ob.push({ name:'',id:count +1  })
        this.props.handleRulesChange(rules,count+2)
        //this.setState({rules,id:this.state.id+1})
    }

    modCondition = (id,newval) =>{
        const {rules} = this.state
        const {count} = this.props
        const ob = this.getID(id,rules)
        if(typeof ob === 'object' && 'all' in ob){
            ob[newval] = {1:ob['all']}
            delete ob['all']

        }else if(typeof ob ==='object' && 'any' in ob){
            ob[newval] = ob['any'][Object.keys(ob['any'])[0]]
            delete ob['any']
        }
        this.props.handleRulesChange(rules,count)
//        this.setState({rules})
    }

    modAny = (id,newval) => {
        const {rules} = this.state
        const {count} = this.props

        const ob = this.getID(id,rules)
        if(typeof ob==='object' && 'any' in ob){
            const delkey = Object.keys(ob['any'])[0]
            ob['any'][newval] = ob['any'][delkey]
            delete ob['any'][delkey]

        }
        this.props.handleRulesChange(rules,count)
        // this.setState({rules})
    }

    addCondition = (obid) =>{
        
        const {rules} = this.state
        const {count} = this.props

        const ob = this.getID(obid,rules)
        ob.push({'all':[count+4],'then':[count+2],'else':[count+3],id:count+1})
        this.props.handleRulesChange(rules,count+5)
        // this.setState({rules,id:this.state.id+4})
    }

    addMulti = (obid) => {
        const {rules} = this.state
        const {count} = this.props

        const ob = this.getID(obid,rules)
        ob.push({'multi_thread':[count+2],id:count+1})
        this.props.handleRulesChange(rules,count+3)
        // this.setState({rules,id:id+2})
    }

    modRule = (id,newval) =>{
        const {rules} = this.state
        const {count} = this.props

        const ob = this.getID(id,rules)
        ob['name'] = newval
        this.props.handleRulesChange(rules,count)
        // this.setState({rules})
    }

  

    //Data deletion functions
    delData = (id,parentId) =>{
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
        this.props.handleRulesChange(rules,this.props.count)
        // this.setState({rules})

    }



   
    render() {
        return (
            <React.Fragment>
                <Form.Group>
                    <Form.Label column sm ={3}>Rule Condition</Form.Label>
                    
                    
                    <ListGroup>
                    {
                        <RuleArr read={this.props.read} data={this.state.rules} rule_list={this.props.rule_list} modRule={this.modRule} delData={this.delData} parentId={null} addCondition={this.addCondition} addMulti={this.addMulti} addRule={this.addRule} modAny= {this.modAny} modCondition={this.modCondition}  />
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
                    
                    <Form.Control required disabled={this.props.read} as='select' value={data['name'] } onChange={event=>this.props.modRule(data['id'],event.target.value)} >
                        <option hidden value="">Select Rule</option>
                        {
                            rule_list.map(ele => <option value={ele}>{ele}</option>)
                        }
                    </Form.Control>
                    </Col>
                    <Col>
                        <Button disabled = {this.props.read} variant='outline-danger' onClick={()=>this.props.delData(data['id'],this.props.parentId)} >Delete</Button>
                    </Col>
                    </Row></ListGroup.Item>
            </React.Fragment>
        )
    }
}

class Multi extends Component {



    render() {
        const {data,rule_list,modRule,delData,addCondition,addMulti,addRule,modCondition,modAny,read} = this.props
        return(
            <React.Fragment>
                <ListGroup.Item>
                <Row>
                <Col sm={2}>
                    <Form.Label>Multithreaded</Form.Label>
                </Col>
                <Col sm ={6}>
                    <RuleArr read = {read} data={data['multi_thread'] } rule_list={rule_list} modRule={modRule} delData={delData}  parentId={data['id']}  addCondition={addCondition} addMulti={addMulti} addRule={addRule} modCondition={modCondition} modAny={modAny}/>
                </Col>
                <Col>
                    <Button disabled={read} variant='outline-danger' onClick={()=>this.props.delData(data['id'],this.props.parentId)} >Delete</Button>
                </Col>
                </Row></ListGroup.Item>
            </React.Fragment>
        )
    }
}

class Conditional extends Component{

    renderData = val => {
        const {data,rule_list,modRule,delData,addCondition,addMulti,addRule,modCondition,modAny,read} = this.props
        if(data[val]){
            if(val==='any'){
              
                return <RuleArr read={read} data={data[val][Object.keys(data['any'])[0]]} rule_list = {rule_list} modRule={modRule} delData={delData} parentId={data['id']}  addCondition={addCondition} addMulti={addMulti} addRule={addRule} modCondition={modCondition} modAny={modAny}/>
            }
            else{
                return <RuleArr read={read} data={data[val]} rule_list={rule_list} modRule={modRule} delData={delData}  parentId={data['id']}  addCondition={addCondition} addMulti={addMulti} addRule={addRule} modCondition={modCondition} modAny={modAny}/>
            }
        }
    }


    render(){
        const {data,read} = this.props

        return(
            <React.Fragment>
                <ListGroup.Item>
                <Row>
                    <br />
                    <ListGroup.Item>
                    <Col>
                        <Form.Control disabled={read} as='select' value={ 'all' in data?'all':'any' } onChange={e => this.props.modCondition(data['id'],e.target.value)}>
                            <option value='all'>all</option>
                            <option value='any'>any</option>
                        </Form.Control>
                        <Col hidden={'any' in data?false:true}>
                            <Form.Control disabled={read} type = 'text' value={ 'any' in data ? Object.keys(data['any'])[0]:'' } onChange={event=>this.props.modAny(data['id'],event.target.value)}/>
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
                    <Col><Button disabled={read} variant='outline-danger' onClick={()=>this.props.delData(data['id'],this.props.parentId)}>Delete </Button></Col>

                    </ListGroup.Item>
                </Row></ListGroup.Item><br />
            </React.Fragment>
        )
    }
}

class RuleArr extends Component{


    renderRules = (data) =>{
        const {rule_list,modRule,delData,addCondition,addMulti,addRule,modCondition,modAny,read} = this.props
        const display = data.map(ele => {
            if(Number.isInteger(ele)){}
                
            else if(typeof ele === 'object' && 'name' in ele){
                return <RuleVar read={read} data={ele} rule_list={rule_list} modRule={modRule} delData={delData} parentId={data[0]} modCondition={modCondition} modAny={modAny}/>
            }
            else if(typeof ele === 'object' && 'multi_thread' in ele){
                return <Multi read={read} data={ele} rule_list={rule_list} modRule={modRule} delData={delData} parentId={data[0]} addCondition={addCondition} addMulti={addMulti} addRule={addRule} modCondition={modCondition} modAny={modAny}/>
            }else if(typeof ele === 'object' && ('all' in ele || 'any' in ele)){
                return <Conditional read={read} data={ele} rule_list={rule_list} modRule={modRule} delData={delData} parentId={data[0]}  addCondition={addCondition} addMulti={addMulti} addRule={addRule} modCondition={modCondition} modAny={modAny}/>
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
                        <Dropdown.Toggle disabled={this.props.read} variant='outline-success' id = 'add'>Add</Dropdown.Toggle>
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










