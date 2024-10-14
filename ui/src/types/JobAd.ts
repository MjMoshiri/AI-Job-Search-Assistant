export interface JobAd {
    id: string;
    date_added: Date;
    description: string;
    link: string;
    is_qualified: boolean;
    user_reasoning: string;
    has_applied: boolean;
    resume_notes: string;
    title: string;
    company: string;
    date_applied: Date;
}