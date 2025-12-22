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
  entryIdx?: string;
  bulletIdx?: string;
  original: string;
  updated: string;
  explanation: string;
}