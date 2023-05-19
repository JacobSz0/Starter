import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import AccountSignupForm from "./AccountSignupForm.js";
import Nav from "./Nav.js";
import { useToken, AuthProvider } from "./Authentication.js";
import MainPage from "./MainPage.js";
import AccountLoginForm from "./AccountLoginForm.js";
import Foot from "./Foot"
import React from 'react';

function GetToken() {
  useToken();
  return null;
}

function App() {
  const domain = /https:\/\/[^/]+/;
  const basename = process.env.PUBLIC_URL.replace(domain, '');

  return (
    <div className="bg">
    <BrowserRouter basename={basename}>
      <AuthProvider>
        <GetToken />
        <Nav />
        <div className="container">
          <Routes>
            <Route path="/" element={<MainPage />} />
            <Route path="account" element={<AccountSignupForm />} />
            <Route path="/login" element={<AccountLoginForm />} />
          </Routes>
        </div>
        <Foot/>
      </AuthProvider>
    </BrowserRouter>
    </div>
  );
}

export default App;
