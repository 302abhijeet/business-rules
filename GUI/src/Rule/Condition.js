import React, { Component } from 'react'
import {Form,Row,Col,Button} from'react-bootstrap'


export class Condition extends Component {
    
    componentWillMount = () =>{
        this.setState({ conditions:this.props.conditions})
    }

    componentWillReceiveProps = nextProps =>{
        if(nextProps !== this.props){
            this.setState({ conditions:this.props.conditions})
        }
    }

    addCondition = () =>{
        
    }

    addSubCondition = () => {

    }

    state = {
        conditions:{
            'all':[]
        }
    }
    
    render() {
        return (
            <React.Fragment>
                <Form.Group>
                    <Form.Label>Conditions</Form.Label>
                    <SubCond variables={this.props.variables}  conditions={this.props.conditions} read={this.props.read} addCondition={this.addCondition}/> 
                </Form.Group>
                

            </React.Fragment>
        )
    }
}

export default Condition



class CondVar extends Component {


    componentWillMount = () => {
        const {cond} = this.props
       

        if(cond!=={}){
            let sc=false,n1 = cond['name'][0],n2
            if(cond['value']===null){
                sc = true
                n2 = cond['name'][1]
            }
            
            this.setState({
                name:cond['name'],
                operator:cond['operator'],
                value:cond['value'],
                second_val:sc,
                name1:n1,
                name2:n2
            })
        }
    }

    componentWillReceiveProps = nextProps => {
        if(nextProps!==this.props){
            const {cond} = this.props
       

        if(cond!=={}){
            let sc=false,n1 = cond['name'][0],n2
            if(cond['value']===null){
                sc = true
                n2 = cond['name'][1]
            }
            
            this.setState({
                name:cond['name'],
                operator:cond['operator'],
                value:cond['value'],
                second_val:sc,
                name1:n1,
                name2:n2
            })
        }
        }
    }


    state={
        name:[],
        operator:'greater_than',
        value:'',
        second_val:false,
        name1:'',
        name2:''
    }

    changeSelect = event => {
        const {name2,name1} = this.state
        if(event.target.name === 'name1'){
            this.setState( {name1:event.target.value,name:[event.target.value,name2]})
        }else if( event.target.name ==='name2' ){
            this.setState( {name2:event.target.value,name:[name1,event.target.value]})
        }else{
            this.setState({[event.target.name]:event.target.value})
        }
    }

    changeCheck = event =>{
        this.setState({ [event.target.name] : !this.state[event.target.name]})
    }

    changeText = event =>{
        this.setState({ [event.target.name]:event.target.value })
    }

    render() {
        const var_list = this.props.variables
        const {read} = this.props
        return(
            
            <React.Fragment>
               <Form.Group>
                <Row>
                    <Col sm={1}></Col>
                    <Col sm={2}>
                        <Form.Control as='select' onChange={this.changeSelect} name='name1' value={this.state.name1} disabled={read}>
                            <option value={null} hidden selected>Select variable</option>    
                            {
                                var_list.map(ele => <option value={ele}>{ele}</option>)
                            }
                        </Form.Control>    
                    </Col>
                    <Col sm={2}>
                        <Form.Control as='select' onChange={this.changeSelect} name='operator' value={this.state.operator} disabled={read}>
                            <option value={null} hidden selected>Select operator</option>
                            <option value ='greater_than'>Greater than</option>
                            <option value ='less_than'>Less than</option>
                            <option value ='equal_to'>Equal to</option>
                        </Form.Control>
                    </Col>    
                    <Col sm={2}>
                            <Form.Label>Select another variable</Form.Label>
                            <Form.Check checked={this.state.second_val} onChange={this.changeCheck} name='second_val' disabled={read} />
                    </Col>
                    
                    <Col sm ={2} hidden={this.state.second_val}>
                        <Form.Control type='text' placeholder='Enter value' value={this.state.value} onChange={this.changeText} name='value' disabled={read}/>
                    </Col>
                    <Col sm ={2} hidden={!this.state.second_val}>
                        <Form.Control as='select' name='name2' value={this.state.name2} onChange={this.changeSelect} disabled={read}> 
                            <option value={null} hidden selected>Select variable</option>    
                            {
                                var_list.map(ele => <option value={ele}>{ele}</option>)
                            }
                        </Form.Control>

                    </Col>
                </Row>
                    
               </Form.Group>
              
                
            </React.Fragment>
        )
    }
}


class SubCond extends Component {
    

    componentWillMount = () =>{
        const {conditions } = this.props
        //condition dictionary has a all or any condition
        if( conditions['all'] )
            this.setState({ sub_cond:{ 
                all:conditions['all']
            }, selected_val:'all'  })   
        
        else if(conditions['any'])
            this.setState({ sub_cond:{ 
                any:conditions['any']
            }, selected_val:'any'  })  
    }

    componentWillReceiveProps = nextProps =>{
        if(this.props!==nextProps){
            const {conditions } = nextProps
            //condition dictionary has a all or any condition
            if( conditions['all'] )
                this.setState({ sub_cond:{ 
                    all:conditions['all']
                }, selected_val:'all' })   
            
            else if(conditions['any'])
                this.setState({ sub_cond:{ 
                    any:conditions['any']
                }, selected_val:'any' })  
        }
    }


    state={
        
        sub_cond:{},
        selected_val:''
    }
    changeVal = event => {
        this.setState({[event.target.name]:event.target.value})
    }

    addCondition=()=>{
        const {sub_cond,selected_val} = this.state
        const newCond = {
            name:[],
            value:'',
            operator:''
        }
        let newsc = sub_cond
        if(selected_val==='all' || selected_val==='any'){
            if(!sub_cond[selected_val])
                newsc[selected_val]=[]
            console.log(newCond)
            newsc[selected_val].push(newCond)
            this.setState({sub_cond:newsc})
        }
       
        
    }
    addSubCondition=()=>{
        // const { sub_cond , selected_val} =this.state
        // let newsc=sub_cond
        // if(selected_val==='all' || selected_val==='any')
        //     if(!sub_cond[selected_val])
        //         newsc[selected_val]=[]
        // newsc[selected_val].push({'all':[]})
        
        // this.setState({sub_cond:newsc})
        // }    

        this.props.addSubCondition('type')
    }

    render() {
        const {variables,read} = this.props
        const {sub_cond,selected_val} = this.state
        let sc,conds 
        if(sub_cond[selected_val]){
            sc =sub_cond[selected_val].map(ele => {
                if(ele['all'] || ele['any']){
                    return (
                        <SubCond variables={variables} conditions={ele} read={read}/>
                    )

            }})
            conds = this.state.sub_cond[this.state.selected_val].map(ele => {
                if(!ele['all'] && !ele['any']){
                    return (
                        <CondVar variables={variables} read={read} cond={ele}/>
                    )
                }
                

            })
        }



        
        return(

            <React.Fragment>
                <Form.Group>
                    <Row>
                        <Col sm={2}>
                        <Form.Control as = 'select' value={this.state.selected_val} onChange={this.changeVal} name='selected_val' disabled={read}>
                            <option value={null} selected  hidden>Select a condition</option>
                            <option value='all'>all</option>
                            <option value = 'any'>any </option>
                        </Form.Control>
                        </Col>
                        <Col sm={4}>
                            <Button variant='outline-dark' onClick={this.addCondition} disabled={read}>Add Condition</Button>
                        </Col>
                        <Col sm={4}>
                            <Button variant = 'outline-dark' onClick={this.addSubCondition } disabled={read}>Add Sub-Condition</Button>
                        </Col>

                    </Row>
                    {/** Render all the conditions and subconditions */}
                    <Row>
                        <Col sm={1}></Col>
                        <Col>
                        {
                            
                        conds
                    }</Col>
                    </Row>
                    {/** Render all the condition for the sub */}
                    <Row>
                        <Col sm={1}></Col>
                        <Col>
                            {
                                sc
                            }
                        </Col>
                    </Row>
                      
                </Form.Group>
               
            </React.Fragment>
        )
    }
}

