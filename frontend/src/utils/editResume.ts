import type { Resume, Suggestion } from "../types"

// applies a suggestion
export function applySuggestion( resume: Resume, s: Suggestion ): Resume {
    const next: Resume = { ...resume };
    const { section, entryIdx, bulletIdx, updated } = s;

    switch( section ) {
        case "languages":
        case "technologies": {
            const field = section === "languages" ? "languages" : "technologies";
            const original = (s.original ?? "").trim();
            const updatedTrimmed = updated.trim();

            next[field] = Array.isArray(next[field]) ? [...next[field]!] : [];

            const isAdd = original === "" && updatedTrimmed !== "";
            const isRemove = original !== "" && updatedTrimmed === "";
            const isReplace = original !== "" && updatedTrimmed !== "";

            if (isAdd) {
                next[field]!.push(updatedTrimmed);
            } else if (isRemove) {
                const removeIdx = next[field]!.findIndex(s => s.trim() === original);
                if (removeIdx >= 0) {
                    next[field]!.splice(removeIdx, 1);
                }
            } else if (isReplace) {
                const replaceIdx = next[field]!.findIndex(s => s.trim() === original);
                if (replaceIdx >= 0) {
                    next[field]![replaceIdx] = updatedTrimmed;
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
        case "languages":
        case "technologies": {
            const field = s.section === "languages" ? "languages" : "technologies";
            const original = (s.original ?? "").trim();
            const updated = (s.updated ?? "").trim();
            const isAdd = original === "" && updated !== "";

            if (isAdd) return true;

            const arr = resume[field];
            return (
                typeof s.entryIdx === "number" &&
                Array.isArray(arr) &&
                s.entryIdx >= 0 &&
                s.entryIdx < arr.length
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
