import React, { Component } from 'react'
import axios from 'axios'

const Context = React.createContext()


export  class Provider extends Component {
    
    state = {
        rules:[],
        variables:{},
        actions:[],
        data_sources:[],
        use_cases:[]

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
        //set the response to be the state
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