export interface Job {
  id: string;
  title: string;
  position_level?: string;
  company?: string;
  location?: string;
  description?: string;
  url: string;
}

export interface Suggestion {
  section: string;
  entryIdx?: number;
  bulletIdx?: number;
  original: string;
  updated: string;
  explanation: string;
}

export interface Heading {
  name?: string | null;
  phone?: string | null;
  email?: string | null;
  location?: string | null;
  linkedin?: string | null;
  github?: string | null;
}

export interface EducationEntry {
  school?: string | null;
  location?: string | null;
  degree?: string | null;
  start?: string | null;
  end?: string | null;
}

export interface Experience {
  company?: string | null;
  title?: string | null;
  location?: string | null;
  start?: string | null;
  end?: string | null;
  details: string[];
}

export interface Project {
  name?: string | null;
  description: string[];
  tech?: string[] | null;
  dateRange?: string | null;
}

export interface Resume {
  heading?: Heading | null;
  summary?: string | null;
  languages?: string[] | null;
  technologies?: string[] | null;
  education?: EducationEntry[] | null;
  experience?: Experience[] | null;
  projects?: Project[] | null;
}
