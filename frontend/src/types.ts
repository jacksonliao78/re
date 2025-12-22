export interface Job {
  id: string;
  title: string;
  position_level ?: string
  company?: string;
  location?: string;
  description?: string;
  url?: string;
}