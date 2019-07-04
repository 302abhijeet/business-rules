import React, { Component } from 'react'

export class FormVar extends Component {
    
    state = {
        name:'',
        field:'',
        label:'',
        options:'',
        formulae:'',
        input_method:{
            DataSource:'',
            command:'',
            evaluation:'',
            start:'',
            end:''
        },
        multi_thread:true
    }
    
    
    handleTextChange = event => {
        this.setState({ [event.target.name] : event.target.value })
    }

    
    
    render() {
        return (
            <React.Fragment>
                <h1>Variable</h1>
                <form>
                <label>
                    Name: 
                    <input name= 'name' type = "text" value = {this.state.name} onChange={this.handleTextChange} />
                </label><br />
                <label>
                    Field: 
                    <input name= 'field' type = "text" value = {this.state.field} onChange={this.handleTextChange} />
                </label><br />
                <label>
                    Label: 
                    <input name= 'label' type = "text" value = {this.state.label} onChange={this.handleTextChange} />
                </label><br />
                <label>
                    Option: 
                    <input name= 'option' type = "text" value = {this.state.option} onChange={this.handleTextChange} />
                </label><br />
                <label>
                    Formulae: 
                    <input name= 'formulae' type = "text" value = {this.state.formulae} onChange={this.handleTextChange} />
                </label><br />
                 <h6>Input Method:</h6><br />
                 <label>
                     Data Source: 
                     <select value = {this.state.DataSource} onChange={this.handleChange}>
                         <option value=""></option>
                         <option value=""></option>
                         <option value=""></option>
                         <option value=""></option>
                     </select>
                 </label>
                    
                </form>
            </React.Fragment>
        )
    }
}

export default FormVar
