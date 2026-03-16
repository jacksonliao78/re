import '../App.css';

interface ResumeEditorProps {
  className?: string;
}

export default function ResumeEditor({ className = '' }: ResumeEditorProps) {
  // PDF rendering is driven by the <object> tag src, which points to the backend
  // /resume/render-pdf endpoint. We POST the resume JSON and stream back a blob
  // URL from a small helper in the parent component; for now this component just
  // serves as a placeholder container. The actual PDF viewer is implemented in
  // a dedicated ResumeViewer component.
  return (
    <div className={`resume-editor ${className}`}>
      <div className="resume-editor-wrapper">
        {/* The actual PDF viewer is rendered by ResumeViewer in App.tsx */}
        <div className="editor-placeholder">
          Resume will be rendered as PDF in the viewer.
        </div>
      </div>
    </div>
  );
}
