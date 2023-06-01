import { useMemo } from "react"
import { ApiClient } from "./ApiClient"
import { OAuthRediectUrl } from "./Types";

export const Login = () => {
    const client = useMemo(() => ApiClient(), []);

    const onLogin = async () => {
        const data = await client.get("auth/login/");
        const response: OAuthRediectUrl = await data.data
        window.location.href = response.redirect_url;
    }

    return (
    <div className="landing-page">
        <div className="content-wrap">
            <h1 className="main-title">Strava Stats Dashboard</h1>
            <p className="description">Interactively view your Strava Stats!</p>
            <button onClick={onLogin} className="btn-strava">Sign up with Strava</button>
        </div>
        <footer className="landing-footer">
        </footer>
    </div>
    )
}