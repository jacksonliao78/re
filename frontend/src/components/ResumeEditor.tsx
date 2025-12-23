import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { useEffect } from 'react';
import type { Resume } from '../types';
import { resumeToTipTap } from '../utils/editResume';
import '../App.css';

interface ResumeEditorProps {
  resume: Resume;
  editable?: boolean;
  timestamp?: Date | string | number;
  className?: string;
}

export default function ResumeEditor({ resume, editable = false, timestamp, className = '' }: ResumeEditorProps) {
  const editor = useEditor({
    extensions: [StarterKit],
    content: resumeToTipTap(resume),
    editable,
    editorProps: {
      attributes: {
        class: 'resume-editor-content',
      },
    },
  });

  // update editor content when resume changes
  useEffect(() => {
    if (editor && resume) {
      const content = resumeToTipTap(resume);
      editor.commands.setContent(content);
    }
  }, [editor, resume]);

  if (!editor) {
    return <div className="resume-editor-loading">Loading editor...</div>;
  }

  return (
    <div className={`resume-editor ${className}`}>
      {timestamp && (
        <div className="resume-editor-timestamp">
          {timestamp instanceof Date 
            ? timestamp.toLocaleString() 
            : new Date(timestamp).toLocaleString()}
        </div>
      )}
      <div className="resume-editor-wrapper">
        <EditorContent editor={editor} />
      </div>
    </div>
  );
}
