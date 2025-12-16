import React, { useState } from "react";
import { updateQuery } from "../api/jobs";
import { useRef, useCallback } from "react";

const JOB_TYPES = ["Software Engineer", "Data Scientist", "Product Manager", "Business Analyst"];

export default function JobSelector() {
  const [jobType, setJobType] = useState<string>(JOB_TYPES[0]);
  const [isIntern, setIsIntern] = useState<boolean>(false);
  const [isFullTime, setIsFullTime] = useState<boolean>(true);
  const debounceRef = useRef<number | null>(null);

  const sendUpdate = useCallback(
    async (updated: { type: string; intern: boolean; fullTime: boolean }) => {
      try {
        await updateQuery(updated);
      } catch (e: any) {
        console.error("updateQuery failed", e);
      } 
    },
    []
  );

  function onTypeChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const t = e.target.value;
    setJobType(t);
    scheduleUpdate({ type: t, intern: isIntern, fullTime: isFullTime });
  }

  function onInternChange(e: React.ChangeEvent<HTMLInputElement>) {
    const v = e.target.checked;
    setIsIntern(v);
    scheduleUpdate({ type: jobType, intern: v, fullTime: isFullTime });
  }

  function onFullTimeChange(e: React.ChangeEvent<HTMLInputElement>) {
    const v = e.target.checked;
    setIsFullTime(v);
    scheduleUpdate({ type: jobType, intern: isIntern, fullTime: v });
  }
  
  function scheduleUpdate(payload: { type: string; intern: boolean; fullTime: boolean }) {
    if (debounceRef.current) {
      window.clearTimeout(debounceRef.current);
    }
    debounceRef.current = window.setTimeout(() => {
      sendUpdate(payload);
      debounceRef.current = null;
    }, 300);
  }

  return (
    <div className="job-selector">
      <label>
        Job type:
        <select value={jobType} onChange={onTypeChange}>
          {JOB_TYPES.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
      </label>

      <div className="job-checkboxes">
        <label>
          <input type="checkbox" checked={isIntern} onChange={onInternChange} /> Intern
        </label>
        <label>
          <input type="checkbox" checked={isFullTime} onChange={onFullTimeChange} /> Full time
        </label>
      </div>
    </div>
  );
}
