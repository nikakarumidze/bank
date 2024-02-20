import { Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import SignUp from "./pages/SignUp";
import Header from "./components/Header";
import Transactions from "./pages/Transactions";

function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route index element={<Index />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/transactions" element={<Transactions />} />
      </Routes>
    </>
  );
}

export default App;
