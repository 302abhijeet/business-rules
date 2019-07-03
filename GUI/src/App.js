import React from 'react';
import {BrowserRouter,Switch,Route} from 'react-router-dom'
import './App.css';
import Navbar from './layout/Navbar'
import Error from './Error'
//Importing page elements
import Rule from './rule-page/Rule'
import UseCase from './uc-page/UseCase'
import Action from './action-page/Action'
import Variable from './var-page/Variable'
import DataSource from './ds-page/DataSource'


function App() {
  return (
    <BrowserRouter>
      <React.Fragment>
        <Navbar />
        <Switch>
          <Route exact path='/' component = {Rule} />
          <Route exact path='/rule' component = {Rule} />
          <Route exact path='/usecase' component = {UseCase} />
          <Route exact path='/variable' component = {Variable} />
          <Route exact path='/action' component = {Action} />
          <Route exact path='/datasource' component = {DataSource} />
          <Route component={Error}/>
        </Switch>
      </React.Fragment>
    </BrowserRouter>
  );
}



export default App;
