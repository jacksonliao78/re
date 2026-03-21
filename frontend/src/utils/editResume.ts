import type { Resume, Suggestion } from "../types"

export function coerceSuggestionIndex(v: unknown): number | undefined {
    if (v === null || v === undefined) return undefined;
    if (typeof v === "number" && Number.isFinite(v)) return Math.trunc(v);
    if (typeof v === "string" && v.trim() !== "") {
        const n = Number(v);
        if (Number.isFinite(n)) return Math.trunc(n);
    }
    return undefined;
}

// applies a suggestion
export function applySuggestion( resume: Resume, s: Suggestion ): Resume {
    const next: Resume = { ...resume };
    const { section, updated } = s;
    const entryIdx = coerceSuggestionIndex(s.entryIdx);
    const bulletIdx = coerceSuggestionIndex(s.bulletIdx);

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
                const removeIdx = next[field]!.findIndex((item) => item.trim() === original);
                if (removeIdx >= 0) {
                    next[field]!.splice(removeIdx, 1);
                }
            } else if (isReplace) {
                const replaceIdx = next[field]!.findIndex((item) => item.trim() === original);
                if (replaceIdx >= 0) {
                    next[field]![replaceIdx] = updatedTrimmed;
                }
            }
            break;
        }
        case 'experience':
            if (
                entryIdx !== undefined &&
                bulletIdx !== undefined &&
                next.experience &&
                next.experience[entryIdx]
            ) {
                next.experience = [...next.experience];
                next.experience[entryIdx] = {
                    ...next.experience[entryIdx],
                    details: [...next.experience[entryIdx].details]
                };
                next.experience[entryIdx].details[bulletIdx] = updated;
            }
            break;
        case 'projects':
            if (
                entryIdx !== undefined &&
                bulletIdx !== undefined &&
                next.projects &&
                next.projects[entryIdx]
            ) {
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
        case "languages":
        case "technologies": {
            const field = s.section === "languages" ? "languages" : "technologies";
            const original = (s.original ?? "").trim();
            const updatedTrimmed = (s.updated ?? "").trim();
            const isAdd = original === "" && updatedTrimmed !== "";

            if (isAdd) return true;

            const isRemove = original !== "" && updatedTrimmed === "";
            const isReplace = original !== "" && updatedTrimmed !== "";
            const arr = resume[field];
            const stringMatches =
                Array.isArray(arr) &&
                !!original &&
                arr.some((x) => (x ?? "").trim() === original);

            if (!isRemove && !isReplace) return false;
            if (!Array.isArray(arr)) return false;
            return stringMatches;
        }
        case "experience": {
            const exp = resume.experience;
            const ei = coerceSuggestionIndex(s.entryIdx);
            const bi = coerceSuggestionIndex(s.bulletIdx);
            const entry =
                exp &&
                ei !== undefined &&
                ei >= 0 &&
                ei < exp.length
                    ? exp[ei]
                    : undefined;
            const details = entry?.details;
            const detailsIsArray = Array.isArray(details);
            return (
                ei !== undefined &&
                bi !== undefined &&
                !!exp &&
                ei >= 0 &&
                ei < exp.length &&
                !!entry &&
                bi >= 0 &&
                detailsIsArray &&
                bi < details.length
            );
        }
        case "projects": {
            const projs = resume.projects;
            const ei = coerceSuggestionIndex(s.entryIdx);
            const bi = coerceSuggestionIndex(s.bulletIdx);
            const proj =
                projs &&
                ei !== undefined &&
                ei >= 0 &&
                ei < projs.length
                    ? projs[ei]
                    : undefined;
            const desc = proj?.description;
            const descIsArray = Array.isArray(desc);
            return (
                ei !== undefined &&
                bi !== undefined &&
                !!projs &&
                ei >= 0 &&
                ei < projs.length &&
                !!proj &&
                bi >= 0 &&
                descIsArray &&
                bi < desc.length
            );
        }

        default:
            return false;
    }
}
