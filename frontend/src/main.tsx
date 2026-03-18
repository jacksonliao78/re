import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import "./index.css";
import App from "./App.tsx";
import ResumePage from "./pages/ResumePage.tsx";
import TailorPage from "./pages/TailorPage.tsx";
import { AuthContextProvider } from "./contexts/AuthContext.tsx";
import { ResumeContextProvider } from "./contexts/ResumeContext.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <AuthContextProvider>
        <ResumeContextProvider>
          <Routes>
            <Route element={<App />}>
              <Route index element={<ResumePage />} />
              <Route path="tailor" element={<TailorPage />} />
            </Route>
          </Routes>
        </ResumeContextProvider>
      </AuthContextProvider>
    </BrowserRouter>
  </StrictMode>
);
