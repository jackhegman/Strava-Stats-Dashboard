import { SetStateAction, useMemo } from "react";
import { ApiClient } from "./ApiClient";
import { User } from "./Types";
import React from "react";

interface NavBarProps {
    user: User
    setUser: React.Dispatch<SetStateAction<User | undefined>>
}

export const NavBar = (props: NavBarProps) => {
    const client = useMemo(ApiClient, []);
    const { user, setUser } = props;

    const logoutUser = () => {
        client.post("auth/logout/").then(d => {
            setUser(undefined);
        }).catch(err => {
            console.error(err);
            setUser(undefined);
        })
    };

    return (
        <div>
            <div className="top-nav">
                <p>{user.first_name} {user.last_name}</p>
                <button onClick={logoutUser} className="btn-strava">Logout</button>
            </div>
        </div>
    )
}