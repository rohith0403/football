import { Component, createResource, createSignal, createMemo } from 'solid-js';
import styles from "./Routes.module.css";

interface Player {
    id: number;
    name: string;
    age: number;
    club: string
};

const fetch_all_players = async (): Promise<Player[]> => {
    const response = await fetch(`http://localhost:8000/get_all_players`);
    if (!response.ok) throw new Error("Failed to fetch data");
    return response.json();
}


const Players: Component = () => {
    const [search, setSearch] = createSignal("");
    const [selectedClub, setSelectedClub] = createSignal("");

    // Fetching players using createResource
    const [players] = createResource<Player[]>(fetch_all_players);

    const clubs = createMemo<string[]>(() => {
        const data = players() as Player[] | undefined; // Explicitly cast to expected type
        if (!data || players.loading) return [];
        return [...new Set(data.map((player) => player.club))];
    });

    // Filter clubs based on search input and selected league
    const filteredPlayer = createMemo<Player[]>(() => {
        const data = players();
        if (!data || players.loading) return [];
        return data.filter(
            (player: Player) =>
                player.name.toLowerCase().includes(search().toLowerCase()) &&
                (selectedClub() === "" || player.club === selectedClub())
        );
    });
    return (
        <div>
            <h1>Players</h1>
            <p>Welcome to the Players page!</p>
            <div class={styles.controls}>
                <input
                    type="text"
                    placeholder="Search Players..."
                    onInput={(e) => setSearch(e.currentTarget.value)}
                    class={styles.searchBox}
                />
                <select
                    onChange={(e) => setSelectedClub(e.currentTarget.value)}
                    class={styles.dropdown}
                >
                    <option value="">All Clubs</option>
                    {clubs().map((club) => (
                        <option value={club}>{club}</option>
                    ))}
                </select>
            </div>
            <table class={styles.table}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Age</th>
                        <th>Club</th>
                    </tr>
                </thead>
                <tbody>
                    {players.loading ? (
                        <tr>
                            <td colspan="4">Loading...</td>
                        </tr>
                    ) : filteredPlayer().length > 0 ? (
                        filteredPlayer().map((player: Player) => (
                            <tr>
                                <td>{player.id}</td>
                                <td>{player.name}</td>
                                <td>{player.age}</td>
                                <td>{player.club}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colspan="4">No results found</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default Players;