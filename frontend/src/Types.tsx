export interface User {
    first_name: string,
    last_name: string
}

export interface OAuthRediectUrl {
    redirect_url: string
}

export interface StravaStat {
    id: number,
    name: string,
    kudos_count: number,
    average_watts: number,
    average_heartrate: number,
    max_heartrate: number,
    pr_count: number,
    total_elevation_gain: number,
    distance: number,
}