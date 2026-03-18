import { createContext, useState, useContext, useEffect, type ReactNode } from "react";
import { useAuth } from "./AuthContext";
import { getDefaultResume } from "../api/auth";
import { saveResume, loadResume, clearResume } from "../utils/resumeStorage";
import type { Resume } from "../types";

interface ResumeContextType {
  resume: Resume | null;
  originalResume: Resume | null;
  setResume: (r: Resume | null) => void;
  setNewResume: (r: Resume | null) => void;
}

const ResumeContext = createContext<ResumeContextType | undefined>(undefined);

export function ResumeContextProvider({ children }: { children: ReactNode }) {
  const { isAuthenticated, token } = useAuth();
  const [originalResume, setOriginalResume] = useState<Resume | null>(null);
  const [resume, setResume] = useState<Resume | null>(null);

  useEffect(() => {
    if (!isAuthenticated || !token) return;
    getDefaultResume(token)
      .then((r) => {
        if (r) {
          setOriginalResume(r);
          setResume(r);
          saveResume(r);
        }
      })
      .catch(() => {});
  }, [isAuthenticated, token]);

  function setNewResume(r: Resume | null) {
    setOriginalResume(r);
    setResume(r);
    if (r) {
      saveResume(r);
    } else {
      clearResume();
    }
  }

  return (
    <ResumeContext.Provider value={{ resume, originalResume, setResume, setNewResume }}>
      {children}
    </ResumeContext.Provider>
  );
}

export function useResume() {
  const context = useContext(ResumeContext);
  if (context === undefined) {
    throw new Error("useResume must be used within a ResumeContextProvider");
  }
  return context;
}
