import { useEffect, useMemo, useState } from "react";
import { ApiClient } from "./ApiClient";
import { StravaStat } from "./Types";

export const StravaDashboard = () => {
    const client = useMemo(() => ApiClient(), []);
    const [stats, setStats] = useState<StravaStat[]>([]);
    const [page, setPage] = useState<number>(1);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        setLoading(true);
        const loadRides = async () => {
            const res = await client.get(`stats/rides/?page=${page}`);
            return res.data
        };

        loadRides().then(rides => {
            setStats(prev => [...prev, ...rides])
            setLoading(false);
        }).catch(err => {
            console.error(err);
            setLoading(false);
        })
    }, [page, setStats, setLoading])

    return (
        <div className="stat-table">
            {loading ?
                <div id="loading" />
                : <div/>
            }
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Kudos Count</th>
                        <th>Average Watts</th>
                        <th>Average Heartrate</th>
                        <th>Max Heartrate</th>
                        <th>PR Count</th>
                        <th>Elevation Gain</th>
                        <th>Distance</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        stats.map(s =>
                            <tr key={s.id}>
                                <td>
                                    <a target="_blank" href={`https://www.strava.com/activities/${s.id}`}>
                                        {s.name}
                                    </a>
                                </td>
                                <td>{s.kudos_count}</td>
                                <td>{s.average_watts}</td>
                                <td>{s.average_heartrate}</td>
                                <td>{s.max_heartrate}</td>
                                <td>{s.pr_count}</td>
                                <td>{s.total_elevation_gain}</td>
                                <td>{s.distance}</td>
                            </tr>
                        )
                    }
                </tbody>
            </table>
            <div className="load-more-btn">
                <button onClick={() => setPage(prev => prev + 1)} className="btn-strava">Load More</button>
            </div>
        </div>
    )
}