import ResumeUploader from "../components/ResumeUploader";
import ResumeViewer from "../components/ResumeViewer";
import KnowledgePanel from "../components/KnowledgePanel";
import { useResume } from "../contexts/ResumeContext";
import { useAuth } from "../contexts/AuthContext";
import { saveDefaultResume } from "../api/auth";

export default function ResumePage() {
  const { resume, originalResume, setNewResume } = useResume();
  const { token } = useAuth();

  return (
    <div className="resume-page">
      <div className="resume-page-upload">
        <ResumeUploader
          onResumeChange={setNewResume}
          resume={resume}
          originalResume={originalResume}
          onSaveDefault={
            token && originalResume
              ? () => saveDefaultResume(originalResume, token)
              : undefined
          }
        />
        <KnowledgePanel token={token} />
      </div>
      <div className="resume-page-viewer">
        {resume ? (
          <ResumeViewer resume={resume} />
        ) : (
          <div className="editor-placeholder">
            Upload a resume to see it rendered here.
          </div>
        )}
      </div>
    </div>
  );
}
