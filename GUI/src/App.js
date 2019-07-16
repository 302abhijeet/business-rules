import React, { Component } from 'react'
import {BrowserRouter,Switch,Route} from 'react-router-dom'
import DataSource from './DataSource/DataSource'
import Rule from './Rule/Rule'
import Variable from './Variable/Variable'
import Action from './Action/Action'
import UseCase from './UseCase/UseCase'
import Home from './Home/Home'
import Run from './Home/Run'
import Navigation from './Navigation'
import {Provider} from './context'

export class App extends Component {
  render() {
    return (
      <Provider>
      <BrowserRouter>
      <Navigation />

        <Switch>

          <Route exact path='/' component={Home} />
          <Route path='/Run/:type/:name' render = {
              props => (
                  <Run type = {props.match.params.type} name = {props.match.params.name}/>
              )
          }/>
          <Route path='/DataSource/:cat'  render = {
            props => (
              <DataSource cat = {props.match.params.cat} />
            )
          } />
          <Route path='/Rule/:cat'  render = {
            props => (
              <Rule cat = {props.match.params.cat} />
            )
          } />
          <Route path='/Variable/:cat'  render = {
            props => (
              <Variable cat = {props.match.params.cat} />
            )
          } />
          <Route path='/Action/:cat'  render = {
            props => (
              <Action cat = {props.match.params.cat} />
            )
          } />
          <Route path='/UseCase/:cat'  render = {
            props => (
              <UseCase cat = {props.match.params.cat} />
            )
          } />
        </Switch>

      </BrowserRouter></Provider>

    )
  }
}

export default App
