import LandingPage from "./screens/LandingPage";
import {AuthProvider} from "./contexts/AuthContext";


function App() {
  return (
    <div className="App">
        <AuthProvider>
            <LandingPage />
        </AuthProvider>
    </div>
  );
}

export default App;
