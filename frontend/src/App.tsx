import React from "react";
import "./App.scss";
import Routes from "./Routes";
import { AuthProvider } from "./services/auth/AuthProvider";

function App() {
  return (
    <AuthProvider>
      <Routes />
    </AuthProvider>
  );
}

export default App;
