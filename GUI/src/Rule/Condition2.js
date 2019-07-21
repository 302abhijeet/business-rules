import React, { Component } from 'react'
import {Form,Row,Col, Button, ListGroup} from 'react-bootstrap'


export class Condition2 extends Component {
    
    componentWillMount = () =>{
        //give id using recursion
        const cond = this.props.conditions
       if(Object.keys(cond).length===0){
           const ob = {'any':[1]}
           console.log('in this')
            this.setState({
                conditions:ob,
                count:2
            })

       }else{

        let id_count = 1
        let count = 1
        //to support old version
        if(cond['name']){
            cond['id'] = id_count
        }
        // new version
        else{
            if(cond['all'])
                count = this.createID(cond['all'],id_count)
            else if(cond['any'])
                count=this.createID(cond['any'],id_count)
        }

        this.setState({
            conditions:cond,
            read:this.props.read,
            count
        })}
    }
    

    createID = (rootObject,id_count) => {
        if(Array.isArray(rootObject)){
            if(!Number.isInteger(rootObject[0])){
                    
                rootObject.unshift(id_count)
            }
            id_count++

            rootObject.forEach(ele => {
                if(ele['all'])
                    id_count = this.createID(ele['all'],id_count)
                else if(ele['any'])
                    id_count = this.createID(ele['any'],id_count)
                else if(ele['name']){
                    //taking care if leaf nodes / condition nodes
                    ele['id'] = id_count 
                    id_count++
                }
            })
            return id_count
        }
    }

    componentWillReceiveProps = nextProps =>{
        //give id using recursion
        if(nextProps!==this.props){
            const cond = nextProps.conditions
            if(Object.keys(cond).length===0){
                const ob = {'any':[1]}
                console.log('in this')
                 this.setState({conditions:ob,read:nextProps.read,count:2})
     
            }else{
                 const {conditions} = nextProps
                 let cond = conditions
                 let id_count = 1
                 let count = 1
                 //to support old version
                 if(cond['name']){
                     cond['id'] = id_count
                 }
                 // new version
                 else{
                     if(cond['all'])
                         count = this.createID(cond['all'],id_count)
                     else if(cond['any'])
                         count=this.createID(cond['any'],id_count)
                 }
                this.setState({conditions:cond,read:nextProps.read,count})
             }
        }
       
    }
    
    getOb=(rootObject,id)=>{
        if(id===null)
            return rootObject
        if(Array.isArray(rootObject)){
            
            // use stack implementation
            const stack = []
    

            stack.push(rootObject)
            while(stack.length !== 0 ){
                const ob = stack.shift()
                if(Array.isArray(ob)){
                    if(ob[0]===id)
                        return ob
                    ob.forEach(ele => {
                        if(ele['name'])
                            stack.push(ele)
                        else if(ele['any'])
                            stack.push(ele['any'])
                        else if(ele['all'])
                            stack.push(ele['all'])
                    })
                }else{
                    if(ob['id']===id)
                        return ob
                }

            }
            return false
            
        }
    }

    delCondition = (id,parentId) => {
        const cond = this.state.conditions
        let pob
        if(cond['all'])
            pob = this.getOb(cond['all'],parentId)
        else if(cond['any'])
            pob = this.getOb(cond['any'],parentId)

        if(Array.isArray(pob)){
            let ind
            for(let i in pob){

                if(pob[i]['name'] && pob[i]['id']===id){
                    ind = i
                    break
                }
                else if( pob[i]['all']){
                    if(pob[i]['all'][0] === id){
                        ind = i
                        break
                    }
                }
                else if(pob[i]['any']){
                    if(pob[i]['any'][0]===id){
                        ind = i 
                        break
                    }
                }
            }
            pob.splice(ind,1)
            this.props.handleConditionChange(cond,this.state.count)
        }
    }

    createNewCondition = parentId =>{
        console.log('in create new condition')
        console.log(parentId)
        const cond = this.state.conditions
        const newId = this.state.count
        let ob
        if(cond['all'])
            ob = this.getOb(cond['all'],parentId)
        else if(cond['any'])
            ob = this.getOb(cond['any'],parentId)
        console.log(ob)
        if(Array.isArray(ob)){
            ob.push({
                name:[],
                value:null,
                operator:'',
                id:newId
            })
            this.props.handleConditionChange(cond,newId+1)
            
        }
    }

    createNewSubCondition = parentId => {
        console.log('in create new subcondition')
        console.log(parentId)
        const cond = this.state.conditions
        const newId = this.state.count
        let ob
        if(cond['all'])
            ob = this.getOb(cond['all'],parentId)
        else if(cond['any'])
            ob = this.getOb(cond['any'],parentId)
        console.log(ob)
        if(Array.isArray(ob)){
            ob.push({
                'any':[newId],

            })
            this.props.handleConditionChange(cond,newId+1)

            
        }
    }

    changeCondition = (newval,id) => {
        console.log('in change condition')
        
        const cond = this.state.conditions
        let ob
        if(cond['all'])
            ob = this.getOb(cond['all'],id)
        else if(cond['any'])
            ob = this.getOb(cond['any'],id)
        
        if(newval['name1']){
            if(ob['name'].length===0)
                ob['name'].unshift(newval['name1'])
            else    
                ob['name'][0] = newval['name1']
        }   
        else if(newval['name2']){
            if(ob['name'].length<=1)
                ob['name'].push(newval['name2'])
            else       
                ob['name'][1] = newval['name2']
            ob['value']=null
        }
        else if(newval['operator'])
            ob['operator'] = newval['operator']
        
        else if(newval['value']){
            ob['value'] = newval['value']
            if(ob['name'].length===2)
                ob['name'].pop()
        }

        this.props.handleConditionChange(cond,this.state.count)

    }

    changeSubCondition = (newval,id,parentID) => {
        console.log('in change sub condition')
        const cond = this.state.conditions
        let ob,pob
        if(cond['all'])
            ob = this.getOb(cond['all'],id)
        else if(cond['any'])
            ob = this.getOb(cond['any'],id)
        
       
        if(parentID===null){
            pob = cond
            const key = Object.keys(pob)[0]
            pob[newval] = pob[key]
            delete pob[key]
            this.props.handleConditionChange(pob,this.state.count)



        }else{
            if(cond['all'])
                pob = this.getOb(cond['all'],parentID)
            else if(cond['any'])
                pob = this.getOb(cond['any'],parentID)    
            
            if(Array.isArray(pob)){
                console.log(pob)
                // if(newval==='all')
                //     ob = {'any':ob}
                // else    
                //     ob= {'all':ob}
                //     console.log(ob)

                let ind
                for(let ele in pob){
                    
                    if(pob[ele]['all']){
                        if(pob[ele]['all'][0]===id){
                            ind = ele
                            break
                        }
                    }else if(pob[ele]['any']){
                        if(pob[ele]['any'][0]===id){
                            ind = ele
                            break
                        }
                    }
                }
                console.log(ind)
                if(ind>-1){
                    console.log(pob)
                    pob.splice(ind,1)
                    pob.splice(ind,0, {[newval]:ob})
                    console.log(pob)
                    this.props.handleConditionChange(cond,this.state.count)
                }
                
                
            }
        }

    }

    state= {
        conditions:{}
        //count will be the id for the next element
    }

    renderSubConditions = () =>{
        const {variables} = this.props
        const {conditions} = this.state
        if(conditions['all']){
            return <SubCond conditions={conditions['all']} selected_val='all' parentId={null} variables={variables} changeCondition={this.changeCondition} changeSubCondition ={this.changeSubCondition} read={this.state.read} createNewCondition={this.createNewCondition} createNewSubCondition={this.createNewSubCondition} delCondition={this.delCondition}/>
        }
        else if(conditions['any']){
            return <SubCond conditions = {conditions['any']} selected_val = 'any' parentId={null} variables={variables} changeCondition={this.changeCondition} changeSubCondition ={this.changeSubCondition} read = {this.state.read} createNewCondition={this.createNewCondition} createNewSubCondition={this.createNewSubCondition} delCondition={this.delCondition}/>
        }
        return ''
    }
    
    
    render() {

        const {variables,conditions,read} = this.props

        return (
            <React.Fragment>
                <Form.Group>
                    <Form.Label>Conditions</Form.Label>
                    {
                        this.renderSubConditions()
                    }
                    {
                        /**Render simple conditions for old version*/
                    }
                </Form.Group>
                

            </React.Fragment>
        )
    }
}

export default Condition2


class SubCond extends Component {

    renderConditions = () =>{
        const {conditions,variables,changeCondition,changeSubCondition} = this.props
        const show = conditions.map(ele => {
            if(ele['name']){
                return <ListGroup.Item>
                        <Row>
                            <Col><Cond element={ele} variables={variables} changeCondition={changeCondition}  read={this.props.read} delCondition={this.props.delCondition}/></Col>
                            <Col md="auto"><Button variant="outline-danger" onClick={()=>this.props.delCondition(ele['id'],conditions[0])}>Delete</Button></Col>
                        </Row>
                    </ListGroup.Item>
            }
        })
        return show
    }

    renderSubConditions = () => {
        const {conditions,variables,changeCondition,changeSubCondition} = this.props
        const show = conditions.map(ele => {
            if(ele['all']){
                return <ListGroup.Item>
                    <Row>
                        <Col><SubCond conditions={ele['all']} selected_val='all' variables={variables} parentId={conditions[0]} changeCondition={changeCondition} changeSubCondition ={changeSubCondition} read={this.props.read} createNewCondition={this.props.createNewCondition} createNewSubCondition={this.props.createNewSubCondition} delCondition={this.props.delCondition}/></Col>
                        <Col md="auto"><Button variant="outline-danger" onClick={()=>this.props.delCondition(ele['all'][0],conditions[0])}>Delete</Button></Col>
                    </Row>
                </ListGroup.Item>
            }else if(ele['any']){
                return <ListGroup.Item>
                    <Row>
                        <Col> <SubCond conditions={ele['any']} selected_val='any' variables={variables} parentId = {conditions[0]} changeCondition={changeCondition} changeSubCondition ={changeSubCondition} read={this.props.read} createNewCondition={this.props.createNewCondition} createNewSubCondition={this.props.createNewSubCondition} delCondition={this.props.delCondition}/></Col>
                        <Col md="auto"><Button variant="outline-danger" onClick={()=>this.props.delCondition(ele['any'][0],conditions[0])}>Delete</Button></Col>
                    </Row>
                </ListGroup.Item>
            }
        })
        return show
    }

    addCond = () =>{
        
        this.props.createNewCondition(this.props.conditions[0])
    }

    addSubCond = () =>{
        this.props.createNewSubCondition(this.props.conditions[0])
    }

    changeSC = event =>{
        this.props.changeSubCondition(event.target.value,this.props.conditions[0],this.props.parentId)
    }


    render(){
        const {selected_val,read,conditions} = this.props 
        return(
            <React.Fragment>
                <Form.Group>
                    <Row>
                        <Col md="auto">
                        <Form.Control as = 'select' value={selected_val}  name='selected_val' disabled={read} onChange={this.changeSC}>
                            <option value='all'>all</option>
                            <option value = 'any'>any </option>
                        </Form.Control>
                        </Col>
                        <Col md="auto">
                            <Button variant='outline-dark' disabled={read} onClick={this.addCond}>Add Condition</Button>
                        </Col>
                        <Col md="auto">
                            <Button variant = 'outline-dark' disabled={read} onClick={this.addSubCond}>Add Sub-Condition</Button>
                        </Col>
                    </Row>
                    <ListGroup>
                        {
                            this.renderConditions()
                        }
                        {
                            this.renderSubConditions()
                        }
                    </ListGroup>
                </Form.Group>
            </React.Fragment>
        )
    }
}

class Cond extends Component {
    
    state = {
        checked:this.props.element['name'].length===2?true:false
    }
    
    changeCheck = event =>{
        this.setState({[event.target.name]:!this.state.checked})
    }

    changeCond = event => {
        const newOb = {
            [event.target.name]:event.target.value
        }
        this.props.changeCondition(newOb,this.props.element['id'])
    }
    

    render(){
        const {element,variables,read} = this.props
        return(
            <React.Fragment>
               <Form.Group>
                <Row>
                    <Col md="auto">
                        <Form.Control required as='select' name='name1' value={element['name'][0]} disabled={read} onChange = {this.changeCond}>
                            <option value="" hidden selected>Select variable</option>    
                            {
                                variables.map(ele => <option value={ele}>{ele}</option>)
                            }
                        </Form.Control>    
                    </Col>
                    <Col md="auto">
                        <Form.Control required as='select'  name='operator' value={element['operator']} disabled={read} onChange = {this.changeCond}>
                            <option value="" hidden selected>Select operator</option>
                            <option value ='greater_than'>Greater than</option>
                            <option value ='less_than'>Less than</option>
                            <option value ='equal_to'>Equal to</option>
                        </Form.Control>
                    </Col>    
                    <Col md="auto">
                            <Form.Label>Select another variable</Form.Label>
                            <Form.Check checked={this.state.checked} onChange={this.changeCheck} name='checked' disabled={read} />
                    </Col>
                    
                    <Col md="auto" hidden={this.state.checked}>
                        <Form.Control required={!this.state.checked} type='text' placeholder='Enter value' value={element['value']}  name='value' disabled={read} onChange = {this.changeCond}/>
                    </Col>
                    <Col md="auto" hidden={!this.state.checked}>
                        <Form.Control as='select'required={this.state.checked} name='name2' value={element['name'][1]}  disabled={read} onChange = {this.changeCond}> 
                            <option value="" hidden selected>Select variable</option>    
                            {
                                variables.map(ele => <option value={ele}>{ele}</option>)
                            }
                        </Form.Control>

                    </Col>
                </Row>
                    
               </Form.Group>
              
                
            </React.Fragment>
        )
    }
}