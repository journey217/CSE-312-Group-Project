import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Login from './pages/login';
import Registration from './pages/registration';
import Index from './pages/index';
import Navbar from './components/navbar';
import './App.css';

function App() {
  return(
    <>
      <Router>  
        <Navbar />
        <Routes>
          <Route path='/login' element={<Login />} />
          <Route path='/registration' element={<Registration />} />
        </Routes>
      </Router>
    </>
  )
}

export default App;
