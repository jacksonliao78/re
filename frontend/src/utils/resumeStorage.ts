import type { Resume } from "../types";

const STORAGE_KEY = "resume_data";

// save Resume to local storage
export function saveResume(resume: Resume): void {
  try {
    const serialized = JSON.stringify(resume);
    localStorage.setItem(STORAGE_KEY, serialized);
  } catch (error) {
    if (error instanceof Error) {
      console.error("Failed to save resume to localStorage:", error.message);
    } else {
      console.error("Failed to save resume to localStorage:", error);
    }
  }
}


// load Resume from local storage
export function loadResume(): Resume | null {
  try {
    const serialized = localStorage.getItem(STORAGE_KEY);
    if (!serialized) {
      return null;
    }
    const resume = JSON.parse(serialized) as Resume;
    return resume;
  } catch (error) {
    if (error instanceof Error) {
      console.error("Failed to load resume from localStorage:", error.message);
    } else {
      console.error("Failed to load resume from localStorage:", error);
    }
    return null;
  }
}

// clear local storage Resume
export function clearResume(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    if (error instanceof Error) {
      console.error("Failed to clear resume from localStorage:", error.message);
    } else {
      console.error("Failed to clear resume from localStorage:", error);
    }
  }
}

