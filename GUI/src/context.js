import React, { Component } from 'react'
import axios from 'axios'
import { objectTypeAnnotation, throwStatement } from '@babel/types';
import {Redirect} from 'react-router-dom'

const Context = React.createContext()


export  class Provider extends Component {
    
    state = {
        rules:null,
        variables:null,
        actions:null,
        history:null,
        DataSource:null,
        use_cases:null,
        redirect:false
    }

    delData = (ty,newOb)=>{
        axios.post(`http://127.0.0.1:5000/del/${ty}`,JSON.stringify(newOb))
            .then((res)=>{
                console.log(res)
            })
            .catch(err=>console.log(err))
        const datas = this.state[ty]
        const newData = datas.filter(ele => ele['name']!==newOb["name"])
        this.setState({
            [ty]:[...newData],
            redirect:true
        })
    }

    addData = (ty,newOb) =>{
        console.log(newOb)
        axios.post(`http://127.0.0.1:5000/add/${ty}`,JSON.stringify(newOb))
        this.setState({
            [ty]:[...this.state[ty],newOb],
            redirect:true

        })
    }

    modifyData = (ty,newOb)=>{
        axios.post(`http://127.0.0.1:5000/modify/${ty}`,JSON.stringify(newOb))
        const datas = this.state[ty]
        datas.forEach(element => {
            if(element['name']===newOb['name']){
                element = newOb
            }    
        })
        this.setState({
            [ty]:[...datas],
            redirect:true

        })
    }

    
    //fetch data from server here
    componentDidMount(){
        //use axios to get data
        axios.get('http://127.0.0.1:5000/get/variables ')
            .then(res => {
                //console.log(res.data.data)
                this.setState({ variables: res.data.data})
            })
            .catch(err => console.log(err))

        axios.get('http://127.0.0.1:5000/get/DataSource ')
            .then(res => {
                
                this.setState({ DataSource: res.data.data})
            })
            .catch(err => console.log(err))
        
        axios.get('http://127.0.0.1:5000/get/rules ')
            .then(res => {
                
                this.setState({ rules: res.data.data})
            })
            .catch(err => console.log(err))

        axios.get('http://127.0.0.1:5000/get/use_cases ')
            .then(res => {
                
                this.setState({ use_cases: res.data.data})
            })
            .catch(err => console.log(err))
        
        axios.get('http://127.0.0.1:5000/get/actions ')
            .then(res => {
                
                this.setState({ actions: res.data.data})
            })
            .catch(err => console.log(err))

        axios.get('http://127.0.0.1:5000/get/history ')
        .then(res => {
            
            this.setState({ history: res.data.data})
        })
        .catch(err => console.log(err))

    }

    render() {
        return (
            <div>
                <Context.Provider value = {{ value:this.state, addNewData:this.addNewData,addData:this.addData,modifyData:this.modifyData,delData:this.delData}} >
                    {this.props.children}    
                </Context.Provider>       
            </div>
        )
    }
}

export const Consumer = Context.Consumer