import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1 className="text-3xl font-bold">Make Your Data Visible!</h1>
      <button 
        onClick={() => navigate("/main")} 
        className="mt-4 bg-red-500 text-white px-4 py-2 rounded"
      >
        Get Started!
      </button>
    </div>
  );
};

export default Home;