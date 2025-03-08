import { Component, createResource, createSignal, createMemo } from 'solid-js';
import styles from "./Leagues.module.css";

type Club = {
    id: number;
    name: string;
    league: string;
};

const fetch_all_clubs = async () => {
    const response = await fetch(`http://localhost:8000/get_all_clubs`);
    if (!response.ok) throw new Error("Failed to fetch data");
    return response.json();
}

const Clubs: Component = () => {
    const [search, setSearch] = createSignal("");
    const [selectedLeague, setSelectedLeague] = createSignal("");

    // Fetching clubs using createResource
    const [clubs] = createResource(fetch_all_clubs);

    const leagues = createMemo<string[]>(() => {
        const data = clubs() as Club[] | undefined; // Explicitly cast to expected type
        if (!data || clubs.loading) return [];
        return [...new Set(data.map((club) => club.league))];
    });

    // Filter clubs based on search input and selected league
    const filteredClubs = createMemo<Club[]>(() => {
        const data = clubs();
        if (!data || clubs.loading) return [];
        return data.filter(
            (club : Club) =>
                club.name.toLowerCase().includes(search().toLowerCase()) &&
                (selectedLeague() === "" || club.league === selectedLeague())
        );
    });
    return (
        <div>
            <h1>Clubs</h1>
            <p>Welcome to the Clubs page!</p>
            <div class={styles.controls}>
                <input
                    type="text"
                    placeholder="Search Club..."
                    onInput={(e) => setSearch(e.currentTarget.value)}
                    class={styles.searchBox}
                />
                <select
                    onChange={(e) => setSelectedLeague(e.currentTarget.value)}
                    class={styles.dropdown}
                >
                    <option value="">All Leagues</option>
                    {leagues().map((league) => (
                        <option value={league}>{league}</option>
                    ))}
                </select>
            </div>
            {/* Clubs Table */}
            <table class={styles.table}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>League</th>
                    </tr>
                </thead>
                <tbody>
                    {clubs.loading ? (
                        <tr>
                            <td colspan="3">Loading...</td>
                        </tr>
                    ) : filteredClubs().length > 0 ? (
                        filteredClubs().map((club : Club) => (
                            <tr>
                                <td>{club.id}</td>
                                <td>{club.name}</td>
                                <td>{club.league}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colspan="3">No results found</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>

    );
};

export default Clubs;

