import { Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import SignUp from "./pages/SignUp";

function App() {
  return (
    <Routes>
      <Route index element={<Index />} />
      <Route path="/signup" element={<SignUp />} />
    </Routes>
  );
}

export default App;
