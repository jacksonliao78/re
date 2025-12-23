export interface Job {
  id: string;
  title: string;
  position_level ?: string
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

export interface Resume {
  summary?: string | null;
  skills?: string[] | null;
  experience?: string[][] | null;
  projects?: string[][] | null;
};
