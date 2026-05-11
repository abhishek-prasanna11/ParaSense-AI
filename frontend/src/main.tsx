import ReactDOM from "react-dom/client";
import App from "./App";
import Result from "./pages/Result";
import "./index.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/result" element={<Result />} />
    </Routes>
  </BrowserRouter>,
);
