import { Component, createResource } from 'solid-js';
import styles from "./Routes.module.css";

type League = {
    id: number;
    name: string;
};

const fetch_all_leagues = async () => {
    const response = await fetch(`http://localhost:8000/get_all_leagues`);
    if (!response.ok) throw new Error("Failed to fetch data");
    return response.json();
}
const Leagues: Component = () => {
    const [leagues] = createResource(fetch_all_leagues);

    return (
        <div>
            <h1>Leagues</h1>
            <p>Welcome to the Leagues page!</p>
            <table class={styles.table}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                    </tr>
                </thead>
                <tbody>
                    {leagues()?.map((item: League) => (
                        <tr>
                            <td>{item.id}</td>
                            <td>{item.name}</td>
                        </tr>
                    )) ?? (
                            <tr>
                                <td colspan="3">Loading...</td>
                            </tr>
                        )}
                </tbody>
            </table>
        </div>
    );
};

export default Leagues;