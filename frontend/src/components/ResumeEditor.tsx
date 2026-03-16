import '../App.css';

interface ResumeEditorProps {
  className?: string;
}

export default function ResumeEditor({ className = '' }: ResumeEditorProps) {
  return (
    <div className={`resume-editor ${className}`}>
      <div className="resume-editor-wrapper">
        <div className="editor-placeholder">
          Resume will be rendered as PDF in the viewer.
        </div>
      </div>
    </div>
  );
}
