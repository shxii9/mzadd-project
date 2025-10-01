import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import './App.css'

// Components
import Header from './components/Header'
import Hero from './components/Hero'
import FeaturedAuctions from './components/FeaturedAuctions'
import Categories from './components/Categories'
import HowItWorks from './components/HowItWorks'
import Footer from './components/Footer'
import AuctionDetails from './components/AuctionDetails'
import Login from './components/Login'
import Register from './components/Register'
import Profile from './components/Profile'

// Context
import { AuthProvider } from './contexts/AuthContext'
import { SocketProvider } from './contexts/SocketContext'

// Main Home Component
const Home = () => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      <main>
        <Hero />
        <FeaturedAuctions />
        <Categories />
        <HowItWorks />
      </main>
      <Footer />
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <SocketProvider>
        <Router>
          <div className="min-h-screen">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/auction/:id" element={<AuctionDetails />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/profile" element={<Profile />} />
            </Routes>
          </div>
        </Router>
      </SocketProvider>
    </AuthProvider>
  )
}

export default App
