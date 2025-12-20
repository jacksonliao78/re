import React, { useState } from "react";

type SelectorPayload = {
  type: string
  intern: boolean
  fullTime: boolean
};

type Props = {
  onChange?: (payload: SelectorPayload) => void;
};

const JOB_TYPES = ["Software Engineer", "Data Scientist", "Product Manager", "Business Analyst"];

export default function JobSelector( { onChange }: Props ) {
  const [jobType, setJobType] = useState<string>(JOB_TYPES[0]);
  const [isIntern, setIsIntern] = useState<boolean>(false);
  const [isFullTime, setIsFullTime] = useState<boolean>(true);

  function notify(payload: SelectorPayload) {
    onChange?.(payload);
  }

  function onTypeChange(e: React.ChangeEvent<HTMLSelectElement>) {
    const t = e.target.value;
    setJobType(t);
    notify({ type: t, intern: isIntern, fullTime: isFullTime });
  }

  function onInternChange(e: React.ChangeEvent<HTMLInputElement>) {
    const v = e.target.checked;
    setIsIntern(v);
    notify({ type: jobType, intern: v, fullTime: isFullTime });
  }

  function onFullTimeChange(e: React.ChangeEvent<HTMLInputElement>) {
    const v = e.target.checked;
    setIsFullTime(v);
    notify({ type: jobType, intern: isIntern, fullTime: v });
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
