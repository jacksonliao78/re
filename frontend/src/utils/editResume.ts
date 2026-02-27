
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

        resume.experience.forEach(exp => {
            // Experience header with title and company
            const expParts: string[] = [];
            if (exp.title) expParts.push(exp.title);
            if (exp.company) expParts.push(`at ${exp.company}`);
            
            if (expParts.length > 0) {
                content.content!.push({
                    type: 'paragraph',
                    attrs: { class: 'experience-header' },
                    content: [{ type: 'text', text: expParts.join(' ') }],
                });
            }
            
            // Experience details as bullet list
            if (exp.details?.length) {
                content.content!.push({
                    type: 'bulletList',
                    content: exp.details.map(detail => ({
                        type: 'listItem',
                        content: [{ type: 'paragraph', content: [{ type: 'text', text: detail }] }],
                    })),
                });
            }
        });
    }

    if (resume.projects?.length) {
        content.content!.push({
            type: 'heading',
            attrs: { level: 2 },
            content: [{ type: 'text', text: 'Projects' }],
        });

        resume.projects.forEach(proj => {
            // Project name as header
            if (proj.name) {
                content.content!.push({
                    type: 'paragraph',
                    attrs: { class: 'project-header' },
                    content: [{ type: 'text', text: proj.name }],
                });
            }
            
            // Project description as bullet list
            if (proj.description?.length) {
                content.content!.push({
                    type: 'bulletList',
                    content: proj.description.map(desc => ({
                        type: 'listItem',
                        content: [{ type: 'paragraph', content: [{ type: 'text', text: desc }] }],
                    })),
                });
            }
            
            // Tech stack if available
            if (proj.tech?.length) {
                content.content!.push({
                    type: 'paragraph',
                    attrs: { class: 'project-tech' },
                    content: [{ type: 'text', text: `Tech: ${proj.tech.join(', ')}` }],
                });
            }
        });
    }

    return content;
}

// applies a suggestion
export function applySuggestion( resume: Resume, s: Suggestion ): Resume {
    const next: Resume = { ...resume };
    const { section, entryIdx, bulletIdx, updated } = s;

    switch( section ) {
        case "summary":
            next.summary = s.updated;
            break;
        case "skills": {
            const original = (s.original ?? "").trim();
            const updatedTrimmed = updated.trim();

            // Ensure we always have an array to work with
            next.skills = Array.isArray(next.skills) ? [...next.skills] : [];

            const isAdd = original === "" && updatedTrimmed !== "";
            const isRemove = original !== "" && updatedTrimmed === "";
            const isReplace = original !== "" && updatedTrimmed !== "";

            if (isAdd) {
                // Add new skill at the end
                next.skills.push(updatedTrimmed);
            } else if (isRemove) {
                // Remove by value to avoid index-shift bugs
                const removeIdx = next.skills.findIndex(skill => skill.trim() === original);
                if (removeIdx >= 0) {
                    next.skills.splice(removeIdx, 1);
                }
            } else if (isReplace) {
                // Replace by value to avoid index-shift bugs
                const replaceIdx = next.skills.findIndex(skill => skill.trim() === original);
                if (replaceIdx >= 0) {
                    next.skills[replaceIdx] = updatedTrimmed;
                }
            }
            break;
        }
        case 'experience':
            if (entryIdx != null && bulletIdx != null && next.experience && next.experience[entryIdx]) {
                next.experience = [...next.experience];
                next.experience[entryIdx] = {
                    ...next.experience[entryIdx],
                    details: [...next.experience[entryIdx].details]
                };
                next.experience[entryIdx].details[bulletIdx] = updated;
            }
            break;
        case 'projects':
            if (entryIdx != null && bulletIdx != null && next.projects && next.projects[entryIdx]) {
                next.projects = [...next.projects];
                next.projects[entryIdx] = {
                    ...next.projects[entryIdx],
                    description: [...next.projects[entryIdx].description]
                };
                next.projects[entryIdx].description[bulletIdx] = updated;
            }
            break;
    }
    return next;
}

// makes sure a suggestion can actually be applied
export function validSuggestion( resume: Resume, s: Suggestion ): boolean {
    switch( s.section ) {
        case "summary":
            return typeof resume.summary === "string";
        case "skills": {
            const original = (s.original ?? "").trim();
            const updated = (s.updated ?? "").trim();
            const isAdd = original === "" && updated !== "";

            // Add-skill suggestions are always allowed; we append safely.
            if (isAdd) return true;

            // For remove/replace, require a valid index into the current skills array.
            return (
                typeof s.entryIdx === "number" &&
                Array.isArray(resume.skills) &&
                s.entryIdx >= 0 &&
                s.entryIdx < resume.skills.length
            );
        }
        case "experience":
            return (
                typeof s.entryIdx === "number" &&
                typeof s.bulletIdx === "number" &&
                !!resume.experience &&
                s.entryIdx >= 0 &&
                s.entryIdx < resume.experience.length &&
                resume.experience[s.entryIdx] &&
                s.bulletIdx >= 0 &&
                s.bulletIdx < resume.experience[s.entryIdx].details.length
            );
        case "projects":
            return (
                typeof s.entryIdx === "number" &&
                typeof s.bulletIdx === "number" &&
                !!resume.projects &&
                s.entryIdx >= 0 &&
                s.entryIdx < resume.projects.length &&
                resume.projects[s.entryIdx] &&
                s.bulletIdx >= 0 &&
                s.bulletIdx < resume.projects[s.entryIdx].description.length
            );

        default:
            return false;
    }
}