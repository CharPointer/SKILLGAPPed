
import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home";   // First page (landing)
import MainPage from "./SecondPage"; // Second page (plot visualization)


function App() {
  useEffect(() => {
    document.title = "skillGAPped";
  }, []);


  return (
    <Router>
      <Routes>
        {/* Home page (First Page) */}
        <Route path="/" element={<Home />} />

        {/* Main page (Second Page) */}
        <Route path="/main" element={<MainPage />} />
      </Routes>
    </Router>
  );
}

export default App;