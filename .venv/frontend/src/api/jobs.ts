import { apiFetch } from './client'

export async function uploadResume(file: File) {
    const form = new FormData()
    form.append( "resume", file );

    const ret = apiFetch('/resume/upload')
    
}