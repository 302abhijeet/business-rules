import React, { Component } from 'react'

export class FormDS extends Component {
    state = {
        name:'',
        method:'SSH',
        info:{
            host_name:'',
            user_name:'',
            password:null,
            key_filename:''
        },
        variables:[],
        multi_thread:true
        
    }    
    
    renderChange = event =>{
        this.setState({[event.target.name]:event.target.value})
    }
    renderChangeSelect = event =>{
        this.setState({[event.target.name]:event.target.value})
        const val = event.target.value
        if(val === 'SSH'){
            this.setState({
                info:{
                    host_name:'',
                    user_name:'',
                    password:null,
                    key_filename:''
                }
            })
        }
        else if(val === 'API'){
            this.setState({
                info:{
                    request:'',
                    url:'',
                    params:{},
                    data:''
                }
            })
        }
        else if(val === 'data_base'){
            this.setState({
                info:{
                    host_name:'',
                    user_name:'',
                    password:null,
                    data_base:''
                }
            })
        }
    }

    handleInfoChange = event =>{
        this.setState({
             info:{...this.state.info, [event.target.name]:event.target.value}
        })
        if(this.state.info.request === 'get'){
            this.setState({    })
        }
    }


    render() {
        const {selected} = this.props
        if(selected != null){

        }
        let method_data
        if(this.state.method === 'SSH'){
            method_data = <FormDsSSH handleInfoChange={this.handleInfoChange} />
        }else if(this.state.method === 'API'){
            method_data = <FormDsAPI handleInfoChange={this.handleInfoChange}/>
        }else if(this.state.method === 'data_base'){
            method_data = <FormDsDB handleInfoChange={this.handleInfoChange}/>
        }else{
            method_data = ''
        }

        return (
           <form>
               Name:
               <input type='text' name='name' value={this.state.name} onChange={this.renderChange} />
               <br />
               Method:
               <select value= {this.state.method} onChange={this.renderChangeSelect} name='method'>
                   <option  value='SSH'>SSH</option>
                    <option value='data_base'> Database</option>
                    <option value='API'>API</option>
               </select>
               {method_data}
                    
           </form>
        )
    }
}

export default FormDS

class FormDsSSH extends Component{
    render(){

        return(
            <React.Fragment>
                <form>
                    User name:
                    <input type='text' name='user_name' onChange={this.props.handleInfoChange} /><br />
                    Host name:
                    <input type='text' name='host_name' onChange={this.props.handleInfoChange} /><br />
                    Password:
                    <input type='password' name='password' onChange={this.props.handleInfoChange} /><br />
                    Key File Location:
                    <input type='text' name='key_filename' onChange={this.props.handleInfoChange} /><br />
                </form>
            </React.Fragment>
        )
    }
}

class FormDsAPI extends Component{
    state = {
        request : 'post',
        param:{},
        data:''
    }
    
    handleReqTypeChange = event =>{
        if(event.target.name === 'get')
        this.setState({ [event.target.name]: event.target.value})
        this.props.handleInfoChange(event)
    }


    handleParameterChange = event =>{

    }

    render(){
        const request_type = this.state.request

        const style = request_type === 'get'? {display:'none'}:{}
        return(
            <React.Fragment>
                <form>
                    Request Type:
                    <select onChange={this.handleReqTypeChange} name='request'>
                        <option  value='post'>Post</option>
                        <option value='get'> Get</option>
        
                    </select><br />
                    URL:
                    <input type='text' name='url' onChange={this.props.handleInfoChange} /><br />
                    
                    Parameters:
                    {}

                    <br />
                    <div  style = {style}   >
                        Data:
                        <input type='textarea' name='data' onChange={this.props.handleReqTypeChange} />
                    </div>
                </form>
            </React.Fragment>
        )
    }
}

class FormDsDB extends Component{
    render(){
        return(
            <React.Fragment>
                <form>
                    User name:
                    <input type='text' name='user_name' onChange={this.props.handleInfoChange} /><br />
                    Host name:
                    <input type='text' name='host_name' onChange={this.props.handleInfoChange} /><br />
                    Password:
                    <input type='password' name='password' onChange={this.props.handleInfoChange} /><br />
                    Database:
                    <input type='text' name='data_base' onChange={this.props.handleInfoChange} /><br />

                </form>
            </React.Fragment>
        )
    }
}
