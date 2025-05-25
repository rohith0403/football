import React, { useEffect, useMemo, useState } from 'react';

// Define the type for a single Todo item
interface TeamSummary {
  id: number;
  name: string;
  league: string;
}

type SortDirection = 'asc' | 'desc';

/**
 * Teams Component
 * A functional React component that fetches and displays a sortable table of teams.
 * It uses useState for managing component state (teams, loading/error states, and sorting)
 * and useEffect for performing side effects (data fetching).
 */
const Teams: React.FC = () => {
  const [teamSummary, setTeamSummary] = useState<TeamSummary[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [sortColumn, setSortColumn] = useState<keyof TeamSummary | null>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');

  /**
   * useEffect Hook for Data Fetching
   * This hook runs once after the initial render (due to the empty dependency array `[]`).
   * It performs the asynchronous data fetching operation.
   */
  useEffect(() => {
    const fetchTeams = async () => {
      try {
        setLoading(true);
        setError(null); // Clear any previous errors
        const response = await fetch('http://localhost:8080/teams');

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        // Parse the JSON response into an array of Todo objects
        const data: TeamSummary[] = await response.json();
        setTeamSummary(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    // Call the fetchTeams function
    fetchTeams();
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
   * useMemo Hook for Sorted Teams
   * This memoizes the sortedTeams array. It will only re-calculate
   * when 'teams', 'sortColumn', or 'sortDirection' change.
   */
  const sortedTeams = useMemo(() => {
    const sortableItems = [...teamSummary];
    if (sortColumn) {
      sortableItems.sort((a, b) => {
        const aValue = a[sortColumn];
        const bValue = b[sortColumn];
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          return sortDirection === 'asc'
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
        } else if (typeof aValue === 'number' && typeof bValue === 'number') {
          return sortDirection === 'asc'
            ? aValue - bValue
            : bValue - aValue;
        } else if (typeof aValue === 'boolean' && typeof bValue === 'boolean') {
          return sortDirection === 'asc'
            ? (aValue === bValue ? 0 : (aValue ? 1 : -1))
            : (aValue === bValue ? 0 : (aValue ? -1 : 1));
        }
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
          Teams
        </h1>

        {loading && (
          <div className="text-center text-blue-400 text-lg"> {/* Adjusted blue for dark mode */}
            Loading teams...
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
                {/* Map over the sortedTeams array and render each todo item as a table row */}
                {sortedTeams.map((team) => (
                  <tr key={team.id} className="border-b border-gray-600 last:border-b-0 hover:bg-gray-600"> {/* Darker row border and hover effect */}
                    <td className="py-3 px-4 text-sm text-gray-300"> {/* Lighter row text */}
                      {team.id}
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-300"> {/* Lighter row text */}
                      {team.name}
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-300"> {/* Lighter row text */}
                      {team.league}
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
