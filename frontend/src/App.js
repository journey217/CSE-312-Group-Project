import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/login';
import Registration from './pages/registration';
import Navbar from './components/navbar';
import LandingPage from './pages/landingPage';
import './App.css';
import Profile from './pages/profilePage'
import Auction_detail from './pages/auctionDetail';

function App() {


  return (
    <div>
      <Router>
        <Navbar />
        <Routes>
          <Route path='/' element={<LandingPage />} />
          <Route path='/login' element={<Login />} />
          <Route path='/registration' element={<Registration />} />
          <Route path='/profile/' element={<Profile></Profile>} />
          <Route path='/itemDetail' element={<Auction_detail />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App;
