import React, { useState, useEffect, useMemo } from 'react';

// Define the type for a single Todo item
interface TeamSummary {
  id: number;
  name: string;
  league: string;
}

// Define the type for sort direction
type SortDirection = 'asc' | 'desc';

/**
 * Teams Component
 * A functional React component that fetches and displays a sortable table of todos.
 * It uses useState for managing component state (todos, loading/error states, and sorting)
 * and useEffect for performing side effects (data fetching).
 */
const Teams: React.FC = () => {
  // State to store the fetched todos
  const [teamSummary, setTeamSummary] = useState<TeamSummary[]>([]);
  // State to manage the loading status
  const [loading, setLoading] = useState<boolean>(true);
  // State to store any error that might occur during fetching
  const [error, setError] = useState<string | null>(null);
  // State to store the currently sorted column key
  const [sortColumn, setSortColumn] = useState<keyof TeamSummary | null>(null);
  // State to store the current sort direction ('asc' for ascending, 'desc' for descending)
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');

  /**
   * useEffect Hook for Data Fetching
   * This hook runs once after the initial render (due to the empty dependency array `[]`).
   * It performs the asynchronous data fetching operation.
   */
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        // Set loading to true before starting the fetch
        setLoading(true);
        setError(null); // Clear any previous errors

        // Perform the fetch request to the JSONPlaceholder API
        const response = await fetch('http://localhost:8080/players');

        // Check if the response was successful (status code 200-299)
        if (!response.ok) {
          // If not successful, throw an error with the status text
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON response into an array of Todo objects
        const data: TeamSummary[] = await response.json();
        // Update the todos state with the fetched data
        setTeamSummary(data);
      } catch (err: any) {
        // Catch any errors during the fetch or JSON parsing and update the error state
        setError(err.message);
      } finally {
        // Set loading to false once the fetch operation is complete (whether successful or not)
        setLoading(false);
      }
    };

    // Call the fetchTodos function
    fetchTodos();
  }, []); // Empty dependency array means this effect runs only once on mount

  /**
   * handleSort Function
   * This function is called when a column header is clicked.
   * It updates the sortColumn and sortDirection states.
   * @param column The key of the column to sort by (e.g., 'id', 'title').
   */
  const handleSort = (column: keyof TeamSummary) => {
    // If the same column is clicked, toggle the sort direction
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // If a new column is clicked, set it as the sort column and default to ascending
      setSortColumn(column);
      setSortDirection('asc');
    }
  };

  /**
   * useMemo Hook for Sorted Todos
   * This memoizes the sortedTodos array. It will only re-calculate
   * when 'todos', 'sortColumn', or 'sortDirection' change.
   */
  const sortedPlayers = useMemo(() => {
    // Create a shallow copy of the todos array to avoid direct mutation
    const sortableItems = [...teamSummary];

    if (sortColumn) {
      sortableItems.sort((a, b) => {
        const aValue = a[sortColumn];
        const bValue = b[sortColumn];

        // Handle different data types for sorting
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          // Case-insensitive string comparison
          return sortDirection === 'asc'
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
        } else if (typeof aValue === 'number' && typeof bValue === 'number') {
          // Numeric comparison
          return sortDirection === 'asc'
            ? aValue - bValue
            : bValue - aValue;
        } else if (typeof aValue === 'boolean' && typeof bValue === 'boolean') {
          // Boolean comparison (false before true for asc)
          return sortDirection === 'asc'
            ? (aValue === bValue ? 0 : (aValue ? 1 : -1))
            : (aValue === bValue ? 0 : (aValue ? -1 : 1));
        }
        // Fallback for other types or mixed types (shouldn't happen with Todo interface)
        return 0;
      });
    }
    return sortableItems;
  }, [teamSummary, sortColumn, sortDirection]); // Dependencies for memoization

  // Helper function to render sort indicator
  const renderSortIndicator = (column: keyof TeamSummary) => {
    if (sortColumn === column) {
      return sortDirection === 'asc' ? ' ▲' : ' ▼'; // Up or down arrow
    }
    return ''; // No indicator
  };

  // Render the component UI
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4 font-sans"> {/* Darker background */}
      <div className="bg-gray-800 p-8 rounded-lg shadow-xl w-full max-w-4xl"> {/* Darker card background */}
        <h1 className="text-3xl font-bold text-center text-gray-100 mb-6"> {/* Lighter text */}
          Players
        </h1>

        {loading && (
          <div className="text-center text-blue-400 text-lg"> {/* Adjusted blue for dark mode */}
            Loading players...
          </div>
        )}

        {error && (
          <div className="text-center text-red-400 text-lg"> {/* Adjusted red for dark mode */}
            Error: {error}
          </div>
        )}

        {!loading && !error && (
          <div className="overflow-x-auto"> {/* Added for responsive table scrolling */}
            <table className="min-w-full bg-gray-700 border border-gray-600 rounded-md"> {/* Darker table background and border */}
              <thead>
                <tr className="bg-gray-600 border-b border-gray-500"> {/* Darker header background and border */}
                  <th
                    className="py-3 px-4 text-left text-sm font-semibold text-gray-200 uppercase tracking-wider rounded-tl-lg cursor-pointer hover:bg-gray-500"
                    onClick={() => handleSort('id')}
                  >
                    ID {renderSortIndicator('id')}
                  </th>
                  <th
                    className="py-3 px-4 text-left text-sm font-semibold text-gray-200 uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                    onClick={() => handleSort('name')}
                  >
                    Name {renderSortIndicator('name')}
                  </th>
                  <th
                    className="py-3 px-4 text-left text-sm font-semibold text-gray-200 uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                    onClick={() => handleSort('league')}
                  >
                    League {renderSortIndicator('league')}
                  </th>
                </tr>
              </thead>
              <tbody>
                {/* Map over the sortedTodos array and render each todo item as a table row */}
                {sortedPlayers.map((player) => (
                  <tr key={player.id} className="border-b border-gray-600 last:border-b-0 hover:bg-gray-600"> {/* Darker row border and hover effect */}
                    <td className="py-3 px-4 text-sm text-gray-300"> {/* Lighter row text */}
                      {player.id}
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-300"> {/* Lighter row text */}
                      {player.name}
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-300"> {/* Lighter row text */}
                      {player.league}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Teams;
