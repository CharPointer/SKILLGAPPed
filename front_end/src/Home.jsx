import { useNavigate } from "react-router-dom";
import NavBar from "./NavBar.jsx";
import "./Home.css";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="backgroundColor">
        <NavBar></NavBar>
    </div>
        
  );
};

export default Home;