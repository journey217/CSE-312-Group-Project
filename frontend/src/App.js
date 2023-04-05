
import React, {useState, useEffect} from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Login from './pages/login';
import Registration from './pages/registration';
import Navbar from './components/navbar';
import LandingPage from './pages/landingPage';
import './App.css';

function App() {
  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/test").then(
        res => res.json()
    ).then(
        data => {
            console.log(data)
        }
    )
  }, [])

  return(
   <div>
      <Router>
        <Navbar />
        <Routes>
          <Route path='/' element={<LandingPage />} />
          <Route path='/login' element={<Login />} />
          <Route path='/registration' element={<Registration />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App;
