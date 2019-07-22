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
        in_operation:false
    }

    delData = (ty,newOb)=>{
        this.setState({in_operation:true})
        axios.post(`http://127.0.0.1:5000/del/${ty}`,JSON.stringify(newOb))
            .then((res)=>{
                console.log(res)
                const datas = this.state[ty]
                const newData = datas.filter(ele => ele['name']!==newOb["name"])
                alert(`${newOb['name']} deleted`)
                this.setState({
                    [ty]:[...newData],
                   in_operation:false
        })
            })
            .catch(err=>{

                alert(`${newOb['name']} couldn't be deleted`)
                console.log(err)
                this.setState({in_operation:false})

                
            }   
            )
        
    }

    addData = (ty,newOb) =>{
        this.setState({in_operation:true})
        axios.post(`http://127.0.0.1:5000/add/${ty}`,JSON.stringify(newOb))
            .then(res=>{
                alert(`${newOb['name']} added`)
                this.setState({
                    [ty]:[...this.state[ty],newOb],
                    in_operation:false
        
                })
            })

            .catch(
                err=>{
                    alert(`${newOb['name']} couldn't be created`)
                    console.log(err)
                    this.setState({in_operation:false})

                }
            )
       
    
    }

    modifyData = (ty,newOb)=>{
        this.setState({in_operation:true})

        axios.post(`http://127.0.0.1:5000/modify/${ty}`,JSON.stringify(newOb))
        .then(res =>{
            alert(`${newOb['name']} modified`)
            const datas = this.state[ty]
            datas.forEach(element => {
                if(element['name']===newOb['name']){
                    element = newOb
                }    
            })
            this.setState({
                [ty]:[...datas],
                in_operation:false
    
            })
        })
        .catch(err =>{
            alert(`${newOb['name']} couldn't be modified`)
            console.log(err)
            this.setState({in_operation:false})

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