import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/Login';
import SignupPage from './pages/Signup';
import DashboardLayout from './components/DashboardLayout';
import HomePage from './pages/HomePage'
import ProtectedRoute from './components/ProtectedRoute';
import { useSelector } from 'react-redux';

const App = () => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

  return (
    <Router>
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/" element={<DashboardLayout />}>
      <Route
        path="/"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated}>
            <HomePage />
          </ProtectedRoute>
        }
      />
      </Route>
    </Routes>
  </Router>
  )
};

export default App;
