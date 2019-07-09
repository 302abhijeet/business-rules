import React, { Component } from 'react'
import axios from 'axios'
import { objectTypeAnnotation } from '@babel/types';
import {Redirect} from 'react-router-dom'

const Context = React.createContext()


export  class Provider extends Component {
    
    state = {
        rules:null,
        variables:null,
        actions:null,
        data_sources:null,
        use_cases:null

    }

    addNewData = (ty,newOb)=>{
        const st = this.state[ty]
        const key = Object.keys(newOb)[0]
        st[key] = newOb[key]
        for(let k in newOb[key]['info']){
            st[key][k] = newOb[key]['info'][k]
            newOb[key][k] = newOb[key]['info'][k]
        }
        delete st[key]['info']
        delete newOb[key]['info']
        let li
        if(ty==='data_sources')
            li = 'datasource'
        
        axios.post(`http://127.0.0.1:5000/add/${li}`,newOb)
        Redirect('/DataSource/index')
        this.setState({[ty]:st})
        

    }
    
    //fetch data from server here
    componentDidMount(){
        //use axios to get data
        axios.get('http://127.0.0.1:5000/get/variables?id=all ')
            .then(res => {
                //console.log(res.data.data)
                this.setState({ variables: res.data.data})
            })
            .catch(err => console.log(err))

        axios.get('http://127.0.0.1:5000/get/datasource?id=all ')
            .then(res => {
                
                this.setState({ data_sources: res.data.data})
            })
            .catch(err => console.log(err))
        
        axios.get('http://127.0.0.1:5000/get/rule?id=all ')
            .then(res => {
                
                this.setState({ rules: res.data.data})
            })
            .catch(err => console.log(err))

        axios.get('http://127.0.0.1:5000/get/use_case?id=all ')
            .then(res => {
                
                this.setState({ use_cases: res.data.data})
            })
            .catch(err => console.log(err))
        
        axios.get('http://127.0.0.1:5000/get/action?id=all ')
            .then(res => {
                
                this.setState({ actions: res.data.data})
            })
            .catch(err => console.log(err))

    }

    render() {
        return (
            <div>
                <Context.Provider value = {{ value:this.state, addNewData:this.addNewData}} >
                    {this.props.children}    
                </Context.Provider>       
            </div>
        )
    }
}

export const Consumer = Context.Consumer