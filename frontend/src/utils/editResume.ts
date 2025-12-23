
import type { Resume, Suggestion } from "../types"
import type { JSONContent } from '@tiptap/core';

// converts a resume object to TipTap JSON
export function resumeToTipTap( resume: Resume ): JSONContent {
    const content: JSONContent = {
        type: 'doc',
        content: []
    }

    if( resume.summary ) {
        content.content!.push( {
            type: 'paragraph',
            content: [ { type: 'text', text: resume.summary }]
        } )
    }

    if( resume.skills ) {
        content.content!.push( {
            type: 'bulletList',
            content: resume.skills.map( skill => ({ 
                type: 'listItem',
                content: [ { type: 'paragraph', content: [ { type: 'text', text: skill }] }]
            } ) )
        })
    }

    if (resume.experience?.length) {
        content.content!.push({
            type: 'heading',
        attrs: { level: 2 },
        content: [{ type: 'text', text: 'Experience' }],
        });

        resume.experience.forEach(entry => {
            content.content!.push({
                type: 'bulletList',
                content: entry.map(line => ({
                type: 'listItem',
                content: [{ type: 'paragraph', content: [{ type: 'text', text: line }] }],
                })),
            });
        });
    }

    if (resume.projects?.length) {
        content.content!.push({
            type: 'heading',
            attrs: { level: 2 },
            content: [{ type: 'text', text: 'Projects' }],
            });

        resume.projects.forEach(entry => {
            content.content!.push({
            type: 'bulletList',
            content: entry.map(line => ({
            type: 'listItem',
            content: [{ type: 'paragraph', content: [{ type: 'text', text: line }] }],
            })),
        });
        });
    }

    return content;
}

// applies a suggestion
export function applySuggestion( resume: Resume, s: Suggestion ) {

    const next = { ... resume }

    const { section, entryIdx, bulletIdx, updated } = s

    switch( section ) {
        case "summary":
            resume.summary = s.updated
            break;
        case 'skills':
            if (entryIdx != null && next.skills) next.skills[entryIdx] = updated;
            break;
        case 'experience':
            if (entryIdx != null && bulletIdx != null && next.experience)
                next.experience[entryIdx][bulletIdx] = updated;
            break;
        case 'projects':
            if (entryIdx != null && bulletIdx != null && next.projects)
                next.projects[entryIdx][bulletIdx] = updated;
            break;

    }
    return;
}

// makes sure a suggestion can actually be applied
export function validSuggestion( resume: Resume, s: Suggestion ): boolean {
    switch( s.section ) {
        case "summary":
            return typeof resume.summary === "string";
        case "skills":
            return (
                typeof s.entryIdx === "number" &&
                !!resume.skills &&
                s.entryIdx >= 0 &&
                s.entryIdx < resume.skills.length
            );
        case "experience":
        case "projects":
            return (
                typeof s.entryIdx === "number" &&
                typeof s.bulletIdx === "number" &&
                !!resume[s.section] &&
                s.entryIdx >= 0 &&
                s.entryIdx < resume[s.section]!.length &&
                s.bulletIdx >= 0 &&
                s.bulletIdx < resume[s.section]![s.entryIdx].length
            );

        default:
            return false;
    }
}