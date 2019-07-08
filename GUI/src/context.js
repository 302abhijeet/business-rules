import React, { Component } from 'react'
import axios from 'axios'

const Context = React.createContext()


export  class Provider extends Component {
    
    state = {
        rules:null,
        variables:null,
        actions:null,
        data_sources:null,
        use_cases:null

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
                <Context.Provider value = {this.state}>
                    {this.props.children}    
                </Context.Provider>       
            </div>
        )
    }
}

export const Consumer = Context.Consumer